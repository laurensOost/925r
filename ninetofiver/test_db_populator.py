from ninetofiver.models import LeaveType, Company, Location, PerformanceType, WorkSchedule, ContractRole,\
    ContractUser, ContractGroup, Timesheet, ActivityPerformance, ProjectContract, Leave, LeaveDate, \
    ProjectContract, ConsultancyContract, SupportContract, Contract
from django.contrib.auth.models import User
import ninetofiver.management.commands.create_timesheets
import logging
from django.conf import settings
import datetime
import random
from calendar import monthrange
log = logging.getLogger(__name__)


# this fills basic tables with data for debugging purposes
# when modifying, make sure to change all lists related to the object
def populate_basic_tables():
    if not settings.DEBUG:
        log.error('settings.DEBUG is False. Aborting')
        exit(1)

    # LeaveType
    leaves = [
        ('Vacation', 'vacation', False, False),
        ('Sickness', 'sickness', False, True),
        ('Recup', 'recup', True, False),
        ('Unpaid', 'unpaid', False, False),
    ]
    for leave_name, leave_desc, leave_overtime, leave_sickness in leaves:
        lt = LeaveType(
            name=leave_name,
            description=leave_desc,
            overtime=leave_overtime,
            sickness=leave_sickness
        )
        lt.save()

    # Company
    companies = [
        ('Inuits', 'CZ12345678', 'Zamenhofova 150 00 Praha 5', 'CZ', True),
        ('ABC', 'BE12345678', 'Ocean drive 42 2060 Antwerpen', 'BE', False),
    ]
    for company_name, company_vat, company_addr, company_country, company_internal in companies:
        com = Company(
            name=company_name,
            vat_identification_number=company_vat,
            address=company_addr,
            country=company_country,
            internal=company_internal
        )
        com.save()

    # Location
    locations = ['Home', 'Brasschaat HQ']
    for loc_name in locations:
        loc = Location(
            name=loc_name
        )
        loc.save()

    # PerformanceType
    perf_types = [
        ('Normal', 'normal', 1.00),
        ('Overtime', 'overtime', 1.50),
        ('Overtime', 'overtime', 2.00),
    ]
    for pt_name, pt_description, pt_multiplier in perf_types:
        pt = PerformanceType(
            name=pt_name,
            description=pt_description,
            multiplier=pt_multiplier
        )
        pt.save()

    # WorkSchedule
    work_schedules = [
        ('Fulltime (7.6h/day)', 7.60, 7.60, 7.60, 7.60, 7.60, 0.00, 0.00),
        ('Parttime (6.4h/day)', 6.40, 6.40, 6.40, 6.40, 6.40, 0.00, 0.00),
        ('Zero', 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00),
    ]
    for ws_name, ws_monday, ws_tuesday, ws_wednesday, ws_thursday, ws_friday, ws_saturday, ws_sunday in work_schedules:
        ws = WorkSchedule(
            name=ws_name,
            monday=ws_monday,
            tuesday=ws_tuesday,
            wednesday=ws_wednesday,
            thursday=ws_thursday,
            friday=ws_friday,
            saturday=ws_saturday,
            sunday=ws_sunday
        )
        ws.save()

    # ContractRole
    cr = ContractRole(
        name='test_contract_role',
        description='test_contract_role'
    )
    cr.save()


# fills higher amount of test data to all contract/performance-related tables
def populate_performance_tables():
    if not settings.DEBUG:
        log.error('settings.DEBUG is False. Aborting')
        exit(1)

    users = []
    companies = []
    companies_customers = []
    contracts = []
    contract_users = []
    contract_groups = []
    activityperformances = []
    performancetypes = PerformanceType.objects.filter()

    # populate db with users, companies, customers, contract_groups
    # its ok to have smaller no. of records for these tables
    for x in range(1, 101):
        usr = User(
            username='test_user_' + str(x),
            email='test_' + str(x) + '@mail.com'
        )
        users.append(usr)
        usr.save()

        comp = Company(
            vat_identification_number='CZ' + str(x),
            name='test_company_' + str(x),
            address='test_company_' + str(x),
            country='CZ',
            internal=True,
        )
        companies.append(comp)
        comp.save()

        comp_cus = Company(
            vat_identification_number='CZ_cus_' + str(x),
            name='test_company_customer_' + str(x),
            address='test_company_customer_' + str(x),
            country='CZ',
            internal=False,
        )
        companies_customers.append(comp_cus)
        comp_cus.save()

        # ContractGroup
        cg = ContractGroup(
            name='test_contract_group_' + str(x)
        )
        contract_groups.append(cg)
        cg.save()

    # populate contracts & activity performances -> higher number of records is good
    for x in range(1, 501):
        proj_cont = ProjectContract(
            name='test_project_contract_' + str(x),
            description='Test project contract ' + str(x),
            customer=companies_customers[random.randrange(len(companies_customers))],
            company=companies[random.randrange(len(companies))],
            starts_at=get_random_date(datetime.date(2017, 1, 1), datetime.date(2021, 1, 1)),
            ends_at=get_random_date(datetime.date(2021, 9, 9), datetime.date(2030, 1, 1)),
            active=1,
            fixed_fee=round(random.uniform(0, 1000), 2),
        )

        cons_cont = ConsultancyContract(
            name='test_consultancy_contract_' + str(x),
            description='Test consultancy contract ' + str(x),
            customer=companies_customers[random.randrange(len(companies_customers))],
            company=companies[random.randrange(len(companies))],
            starts_at=get_random_date(datetime.date(2017, 1, 1), datetime.date(2021, 1, 1)),
            ends_at=get_random_date(datetime.date(2021, 9, 9), datetime.date(2030, 1, 1)),
            active=1,
            duration=round(random.uniform(0, 100), 1),
            day_rate=round(random.uniform(0, 100), 2),
        )

        supp_cont = SupportContract(
            name='test_support_contract_' + str(x),
            description='Test support contract ' + str(x),
            customer=companies_customers[random.randrange(len(companies_customers))],
            company=companies[random.randrange(len(companies))],
            starts_at=get_random_date(datetime.date(2017, 1, 1), datetime.date(2021, 1, 1)),
            ends_at=get_random_date(datetime.date(2021, 9, 9), datetime.date(2030, 1, 1)),
            active=1,
            day_rate=round(random.uniform(0, 100), 2),
            fixed_fee=round(random.uniform(0, 1000), 2),
        )

        contracts.append(proj_cont)
        contracts.append(cons_cont)
        contracts.append(supp_cont)
        proj_cont.save()
        cons_cont.save()
        supp_cont.save()

    # add contract users
    for usr in users:
        for ctr in contracts:
            cu = ContractUser(
                user=usr,
                contract=ctr,
                contract_role=ContractRole.objects.get()
            )
            contract_users.append(cu)

    ContractUser.objects.bulk_create(contract_users)

    timesheets_maker = ninetofiver.management.commands.create_timesheets.Command()

    timesheets_maker.handle()

    all_timesheets = Timesheet.objects.filter()
    no_of_timesheets = all_timesheets.count()
    # contracts_pure = Contract.objects.filter()
    # Performance
    for x in range(1, 10000):
        curr_timesheet_index = x % no_of_timesheets
        curr_timesheet = all_timesheets[curr_timesheet_index]
        days_in_month = monthrange(curr_timesheet.year, curr_timesheet.month)[1]

        act_perf = ActivityPerformance(
            timesheet=curr_timesheet,
            date=datetime.date(curr_timesheet.year, curr_timesheet.month, random.randint(1, days_in_month)),
            contract=contracts[random.randrange(len(contracts))],
            performance_type=performancetypes[0],
            contract_role=ContractRole.objects.get(),
            description='test_activity_performance_' + str(x),
            duration=1,
            )
        activityperformances.append(act_perf)
        act_perf.save()

    # ActivityPerformance.objects.bulk_create(activityperformances)


def get_random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days

    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)

    return random_date


# fills higher amount of test data to all leave-related tables
def populate_leave_tables():
    if not settings.DEBUG:
        log.error('settings.DEBUG is False. Aborting')
        exit(1)

    leaves = []
    leavedates = []

    # retrieving information from already populated tables we'll be using
    users = User.objects.filter()

    for usr in users:
        for x in range(1, 100):
            lv = Leave(
                user=usr,
                leave_type=LeaveType.objects.get(name='Vacation'),
                description='vacation_test',
            )
            leaves.append(lv)
            lv.save()
