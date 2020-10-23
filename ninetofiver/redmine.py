"""Redmine integration."""
import logging
import datetime
from redminelib import Redmine
from ninetofiver import models, settings


logger = logging.getLogger(__name__)
connector = None


def get_redmine_connector():
    """Get a redmine connector."""
    global connector
    if connector:
        return connector
    
    url = settings.REDMINE_URL
    api_key = settings.REDMINE_API_KEY

    if url and api_key:
        connector = Redmine(url, key=api_key)
        return connector

    logger.debug('No base URL and API key provided for connecting to Redmine')
    return None


def get_redmine_user_choices():
    """Get redmine project choices."""
    choices = [[None, '-----------']]
    redmine = get_redmine_connector()

    if redmine:
        res = redmine.user.all()
        choices += sorted([[x.id, '%s %s [%s, %s]' % (x.firstname, x.lastname, x.login, x.mail)] for x in res],
                          key=lambda x: x[1].lower())

    return choices


def get_redmine_project_choices():
    """Get redmine project choices."""
    choices = [[None, '-----------']]
    redmine = get_redmine_connector()

    if redmine:
        res = redmine.project.all()
        choices += sorted([[x.id, x.name] for x in res], key=lambda x: x[1].lower())

    return choices


def get_user_redmine_id(user):
    """Get redmine user ID for the given user."""
    user_id = None

    if user.userinfo and user.userinfo.redmine_id:
        user_id = user.userinfo.redmine_id

    if (not user_id) and user.email:
        redmine = get_redmine_connector()

        if redmine:
            res = list(redmine.user.filter(name=user.username, limit=2))
            if len(res) == 1:
                user_id = res[0].id

    return user_id


def get_user_redmine_issues(user, status=None):
    """Get assigned Redmine issues for the given user."""
    data = []

    redmine = get_redmine_connector()
    if not redmine:
        return data

    user_id = get_user_redmine_id(user)
    if not user_id:
        logger.debug('No Redmine user ID found for user %s' % user.id)
        return data

    data = list(redmine.issue.filter(assigned_to_id=user_id))

    return data

def _get_all_parent_issues_with_contract(data: list, parent_field = 'issue'):
    """Gets all parent issues of given data and looks deeper for contract."""
    redmine = get_redmine_connector()
    if not redmine:
        return []

    parent_id_set = set()
    for record in data:
        issue = getattr(record, parent_field, None)
        if issue:
            parent_id_set.add(str(issue.id))

    if not parent_id_set:
        return []

    issues = list(redmine.issue.filter(issue_id=','.join(parent_id_set), status_id='*'))
    # For every issue check if we can find contract field and if not try to look deeper
    # For performance reasons we do this deeper look in batches
    deeper_issues = []
    for issue in issues:
        has_contract_field = False
        for custom_field in getattr(issue, 'custom_fields', []):
            if custom_field.name == settings.REDMINE_ISSUE_CONTRACT_FIELD:
                if custom_field.value:
                    has_contract_field = True
            break

        if not has_contract_field:
            deeper_issues.append(issue)

    issues.extend(_get_all_parent_issues_with_contract(deeper_issues, 'parent'))
    return issues

def _get_contract_id_from_redmine_data(issue_id: str, issue_dict: dict):
    """Gets contract id value from issue or parents of issue."""
    issue = issue_dict.get(issue_id, None)
    for custom_field in getattr(issue, 'custom_fields', []):
        if (custom_field.name == settings.REDMINE_ISSUE_CONTRACT_FIELD):
            if (custom_field.value):
                custom_field_value = custom_field.value.split('|')[0]
                return int(custom_field_value)
            break
    parent = getattr(issue, 'parent', None)
    if parent:
        return _get_contract_id_from_redmine_data(parent.id, issue_dict)
    else:
        return None


def get_user_redmine_performances(user, from_date=None, to_date=None):
    """Get available Redmine performances for the given user."""
    data = []

    url = settings.REDMINE_URL
    redmine = get_redmine_connector()
    if not redmine:
        return data

    user_id = get_user_redmine_id(user)
    if not user_id:
        logger.debug('No Redmine user ID found for user %s' % user.id)
        return data

    if not from_date:
        from_date = datetime.date.today()

    if not to_date:
        to_date = datetime.date.today()

    time_entries = list(redmine.time_entry.filter(from_date=from_date, to_date=to_date, user_id=user_id))
    # If we have no time entries, return early
    if len(time_entries) == 0:
        return data

    issues = _get_all_parent_issues_with_contract(time_entries)
    issue_dict = {x.id: x for x in issues}

    # Fetch a list of redmine project IDs and contract ID for the user
    contracts = (models.Contract.objects
                 .filter(contractuser__user=user)
                 .values('redmine_id', 'id'))
    contract_ids = [x['id'] for x in contracts]
    # Contract a dict mapping redmine project IDs to a user's contract IDs
    redmine_contracts = {str(x['redmine_id']): x['id'] for x in contracts}

    # Construct a dict mapping redmine time entry IDs to a user's performance IDs
    time_entry_ids = [x.id for x in time_entries]
    redmine_performances = (models.Performance.objects
                            .filter(timesheet__user=user, redmine_id__in=time_entry_ids)
                            .values('redmine_id', 'id'))
    redmine_performances = {str(x['redmine_id']): x['id'] for x in redmine_performances}

    for entry in time_entries:
        performance_id = redmine_performances.get(str(entry.id), None)

        # The contract ID for the given time entry is determined by:
        # * Looking for a custom field value which is part of the user's contract list
        # * Looking for a redmine project ID which maps to one of the user's contracts
        contract_id = None
        if getattr(entry, 'issue', None):
            contract_id = _get_contract_id_from_redmine_data(entry.issue.id, issue_dict)

        if not contract_id:
            contract_id = redmine_contracts.get(str(entry.project.id), None)

        if (not contract_id) or (contract_id not in contract_ids):
            logger.debug('No contract found for Redmine time entry with ID %s' % entry.id)
            continue

        if getattr(entry, 'issue', None):
            description = '_See [#%s](%s/issues/%s)._' % (entry.issue.id, url, entry.issue.id)
        else:
            description = '_No issue linked._'
        if entry.comments:
            description = '%s\n%s' % (entry.comments, description)

        perf = {
            'id': performance_id,
            'contract': contract_id,
            'redmine_id': entry.id,
            'duration': entry.hours,
            'description': description,
            'date': entry.spent_on,
        }

        data.append(perf)

    return data
