from ninetofiver.models import LeaveType, Company, Location, PerformanceType, WorkSchedule
import logging
log = logging.getLogger(__name__)


# this fills basic tables with data for debugging purposes
# when modifying, make sure to change all lists related to the object
def populate_basic_tables():
    from django.conf import settings
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
