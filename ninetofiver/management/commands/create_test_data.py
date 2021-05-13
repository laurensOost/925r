from django.core.management.base import BaseCommand
from ninetofiver.test_db_populator import TestDBPupulator


class Command(BaseCommand):
    """Fill basic tables with data for debugging purposes"""

    args = ''
    help = 'Fill basic tables with data for debugging purposes'

    def handle(self, *args, **options):
        """Create a new timesheet for the current month for each user."""
        TestDBPupulator().execute()
