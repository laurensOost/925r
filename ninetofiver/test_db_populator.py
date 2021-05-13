import datetime
import logging
import random
from calendar import monthrange
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.auth.models import User

from ninetofiver.models import Timesheet, WorkSchedule, Leave, LeaveType, LeaveDate, Company, ContractGroup,\
    ContractRole, ContractUser, ProjectContract, SupportContract, PerformanceType, ActivityPerformance, Location,\
    ConsultancyContract

log = logging.getLogger(__name__)


def get_random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days

    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)

    return random_date


class TestDBPupulator:
    def __init__(self):
        if not settings.DEBUG:
            log.error('settings.DEBUG is False. Aborting')
            exit(1)

        self.cont_role = None

        self.activity_performances = []
        self.all_timesheets = []
        self.companies = []
        self.companies_customers = []
        self.contract_groups = []
        self.contract_users = []
        self.contracts = []
        self.leaves = []
        self.leavetypes = []
        self.leavedates = []
        self.locations = []
        self.perf_types = []
        self.users = []
        self.work_schedules = []

    def execute(self):
        ''' Order of methods is important '''
        self._populate_basic_tables()
        self._populate_performance_tables()
        self._populate_leave_tables()

    def _populate_basic_tables(self):
        '''
        This fills basic tables with data for debugging purposes
        when modifying, make sure to change all lists related to the object
        '''
        self.leavetypes = [
            ('Vacation', 'vacation', False, False),
            ('Sickness', 'sickness', False, True),
            ('Recup', 'recup', True, False),
            ('Unpaid', 'unpaid', False, False),
        ]
        for leave_name, leave_desc, leave_overtime, leave_sickness in self.leavetypes:
            lt = LeaveType(
                name=leave_name,
                description=leave_desc,
                overtime=leave_overtime,
                sickness=leave_sickness
            )
            lt.save()

        companies_example = [
            ('Inuits', 'CZ12345678', 'Zamenhofova 150 00 Praha 5', 'CZ', True),
            ('ABC', 'BE12345678', 'Ocean drive 42 2060 Antwerpen', 'BE', False),
        ]
        for company_name, company_vat, company_addr, company_country, company_internal in companies_example:
            com = Company(
                name=company_name,
                vat_identification_number=company_vat,
                address=company_addr,
                country=company_country,
                internal=company_internal
            )
            com.save()
            self.companies.append(com)

        locations_examples = ['Home', 'Brasschaat HQ']
        for loc_name in locations_examples:
            loc = Location(
                name=loc_name
            )
            loc.save()
            self.locations.append(loc)

        perf_types_example = [
            ('Normal', 'normal', 1.00),
            ('Overtime', 'overtime', 1.50),
            ('Overtime', 'overtime', 2.00),
        ]
        for pt_name, pt_description, pt_multiplier in perf_types_example:
            pt = PerformanceType(
                name=pt_name,
                description=pt_description,
                multiplier=pt_multiplier
            )
            pt.save()
            self.perf_types.append(pt)

        self.work_schedules = [
            ('Fulltime (7.6h/day)', 7.60, 7.60, 7.60, 7.60, 7.60, 0.00, 0.00),
            ('Parttime (6.4h/day)', 6.40, 6.40, 6.40, 6.40, 6.40, 0.00, 0.00),
            ('Zero', 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00),
        ]
        for ws_name, ws_mon, ws_tue, ws_wed, ws_thu, ws_fri, ws_sat, ws_sun in self.work_schedules:
            ws = WorkSchedule(
                name=ws_name,
                monday=ws_mon,
                tuesday=ws_tue,
                wednesday=ws_wed,
                thursday=ws_thu,
                friday=ws_fri,
                saturday=ws_sat,
                sunday=ws_sun
            )
            ws.save()

    def _populate_performance_tables(self):
        '''
        Fills higher amount of test data to all contract/performance-related tables
        Populate db with users, companies, customers, contract_groups
        '''
        self.cont_role = ContractRole(
            name='test_contract_role',
            description='test_contract_role'
        )
        self.cont_role.save()

        # Its ok to have smaller no. of records for these tables
        for x in range(1, 101):
            usr = User(
                username='test_user_' + str(x),
                email='test_' + str(x) + '@mail.com'
            )
            usr.save()
            self.users.append(usr)

            comp = Company(
                vat_identification_number='CZ00' + str(x),
                name='test_company_' + str(x),
                address='test_company_' + str(x),
                country='CZ',
                internal=True,
            )
            comp.full_clean()
            comp.save()
            self.companies.append(comp)

            comp_cust = Company(
                vat_identification_number='CZ000' + str(x),
                name='test_company_customer_' + str(x),
                address='test_company_customer_' + str(x),
                country='CZ',
                internal=False,
            )
            comp_cust.full_clean()
            comp_cust.save()
            self.companies_customers.append(comp_cust)

            cg = ContractGroup(
                name='test_contract_group_' + str(x)
            )
            cg.save()
            self.contract_groups.append(cg)

        # populate contracts & activity performances -> higher number of records is good
        for x in range(1, 501):
            proj_cont = ProjectContract(
                name='test_project_contract_' + str(x),
                description='Test project contract ' + str(x),
                customer=self.companies_customers[random.randrange(len(self.companies_customers))],
                company=self.companies[random.randrange(len(self.companies))],
                starts_at=get_random_date(datetime.date(2017, 1, 1), datetime.date(2021, 1, 1)),
                ends_at=get_random_date(datetime.date(2021, 9, 9), datetime.date(2030, 1, 1)),
                active=1,
                fixed_fee=round(random.uniform(0, 1000), 2),
            )

            cons_cont = ConsultancyContract(
                name='test_consultancy_contract_' + str(x),
                description='Test consultancy contract ' + str(x),
                customer=self.companies_customers[random.randrange(len(self.companies_customers))],
                company=self.companies[random.randrange(len(self.companies))],
                starts_at=get_random_date(datetime.date(2017, 1, 1), datetime.date(2021, 1, 1)),
                ends_at=get_random_date(datetime.date(2021, 9, 9), datetime.date(2030, 1, 1)),
                active=1,
                duration=round(random.uniform(0, 100), 1),
                day_rate=round(random.uniform(0, 100), 2),
            )

            supp_cont = SupportContract(
                name='test_support_contract_' + str(x),
                description='Test support contract ' + str(x),
                customer=self.companies_customers[random.randrange(len(self.companies_customers))],
                company=self.companies[random.randrange(len(self.companies))],
                starts_at=get_random_date(datetime.date(2017, 1, 1), datetime.date(2021, 1, 1)),
                ends_at=get_random_date(datetime.date(2021, 9, 9), datetime.date(2030, 1, 1)),
                active=1,
                day_rate=round(random.uniform(0, 100), 2),
                fixed_fee=round(random.uniform(0, 1000), 2),
            )

            proj_cont.save()
            cons_cont.save()
            supp_cont.save()
            self.contracts.append(proj_cont)
            self.contracts.append(cons_cont)
            self.contracts.append(supp_cont)

        # add contract users
        for usr in self.users:
            for ctr in self.contracts:
                cu = ContractUser(
                    user=usr,
                    contract=ctr,
                    contract_role=self.cont_role
                )
                cu.save()
                self.contract_users.append(cu)

        self.create_timesheets()

        # add performance
        # 10 for every timesheet, random contracts
        for ts in self.all_timesheets:
            for x in range(1, 11):
                days_in_month = monthrange(ts.year, ts.month)[1]

                act_perf = ActivityPerformance(
                    timesheet=ts,
                    date=datetime.date(ts.year, ts.month, random.randint(1, days_in_month)),
                    contract=self.contracts[random.randrange(len(self.contracts))],
                    performance_type=self.perf_types[0],
                    contract_role=self.cont_role,
                    description='test_activity_performance_' + str(x),
                    duration=1,
                    )
                act_perf.save()
                self.activity_performances.append(act_perf)

    def create_timesheets(self):
        """Create a new timesheet for the current month for each user."""
        today = datetime.date.today()
        next_month = datetime.date.today() + relativedelta(months=1)

        for user in self.users:
            # Ensure timesheet for this month exists
            ts_this_month, _ = Timesheet.objects.get_or_create(
                user=user,
                month=today.month,
                year=today.year
            )

            # Ensure timesheet for next month exists
            ts_next_month, _ = Timesheet.objects.get_or_create(
                user=user,
                month=next_month.month,
                year=next_month.year
            )

            self.all_timesheets.append(ts_this_month)
            self.all_timesheets.append(ts_next_month)

    # fills higher amount of test data to all leave-related tables
    def _populate_leave_tables(self):

        for usr in self.users:
            leave_dates_for_user = []
            for x in range(1, 3):
                lv = Leave(
                    user=usr,
                    leave_type=LeaveType.objects.get(name='Vacation'),
                    description='vacation_test',
                )
                lv.save()
                self.leaves.append(lv)

                # leave length in days
                leave_length = 3

                # load all timesheets for user
                timesheets_for_user = Timesheet.objects.filter(user=usr)
                # select one timesheet for user
                ts = timesheets_for_user[random.randrange(len(timesheets_for_user))]
                k = True
                while k is True:
                    invalid_date_found = False
                    # find a leave date in selected timesheet
                    start_date = get_random_date(datetime.datetime(ts.year, ts.month, 1),
                                                 # potential end date
                                                 datetime.datetime(ts.year, ts.month+1, 1)
                                                 - datetime.timedelta(days=leave_length))  # unknown no. of days in mth
                    # check if user already has leave planned in this date. if so, find another date
                    for pot_day_no in range(0, leave_length):
                        potential_leave_date = start_date + datetime.timedelta(days=pot_day_no)
                        if potential_leave_date not in leave_dates_for_user:
                            continue
                        else:
                            invalid_date_found = True
                            break
                    if invalid_date_found is True:
                        continue
                    else:
                        break
                for day in range(0, leave_length):
                    ld = LeaveDate(
                        leave=lv,
                        timesheet=ts,
                        starts_at=start_date.replace(hour=9, minute=00, second=00) + datetime.timedelta(days=day),
                        ends_at=start_date.replace(hour=17, minute=00, second=00) + datetime.timedelta(days=day),
                    )
                    # adding each day of user's holiday to the list so that holidays never collide
                    leave_dates_for_user.append(start_date + datetime.timedelta(days=day))
                    ld.save()
                    self.leavedates.append(ld)
