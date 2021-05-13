"""Create timesheets."""
import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth import models as auth_models
from dateutil.relativedelta import relativedelta

from ninetofiver.test_db_populator import TestDBPupulator


class Command(BaseCommand):
    """Create a new timesheet for the current month for each user."""

    args = ''
    help = 'Create a new Timesheet for every active user'

    def handle(self, *args, **options):

        TestDBPupulator().create_timesheets()
