from django.core.management.base import BaseCommand
from ninetofiver.test_db_populator import populate_basic_tables, populate_performance_tables
import ninetofiver.management.commands.create_timesheets


class Command(BaseCommand):
    """Fill basic tables with data for debugging purposes"""

    args = ''
    help = 'Fill basic tables with data for debugging purposes'

    def handle(self, *args, **options):
        """Create a new timesheet for the current month for each user."""
        ninetofiver.management.commands.create_timesheets.Command.handle(self)
        populate_basic_tables()
        populate_performance_tables()
