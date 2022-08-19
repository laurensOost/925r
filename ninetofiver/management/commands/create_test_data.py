from django.core.management.base import BaseCommand
from ninetofiver.test_db_populator import TestDBPupulator


class Command(BaseCommand):
    """Fill basic tables with data for debugging purposes"""

    args = ''
    help = 'Fill basic tables with data for debugging purposes'

    def add_arguments(self, parser):
        parser.add_argument(
            "ammount",
            type=str,
            nargs="?",
            choices=['small', 'normal', 'extensive'],
            default="normal"
        )

    def handle(self, *args, **options):
        """Create a new timesheet for the current month for each user."""
        if options["ammount"] == "small":
            TestDBPupulator(10, 50).execute()
        elif options["ammount"] == "normal":
            TestDBPupulator(70, 350).execute()
        elif options["ammount"] == "extensive":
            TestDBPupulator(100, 500).execute()
