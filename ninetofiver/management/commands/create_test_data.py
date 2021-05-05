from django.core.management.base import BaseCommand
from ninetofiver.test_db_populator import populate_basic_tables


class Command(BaseCommand):
    """Fill basic tables with data for debugging purposes"""

    args = ''
    help = 'Fill basic tables with data for debugging purposes'

    def handle(self, *args, **options):
        """Create a new timesheet for the current month for each user."""
        populate_basic_tables()
