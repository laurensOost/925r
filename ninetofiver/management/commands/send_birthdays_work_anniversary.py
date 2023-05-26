"""Send a reminder about birthdays and work anniversary."""
import logging
from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _
import datetime
from ninetofiver import models
from ninetofiver.utils import get_users_with_permission, send_mail


log = logging.getLogger(__name__)


class Command(BaseCommand):
    """Send a reminder about birthdays and work anniversaries."""

    args = ""
    help = "Send a reminder about birthdays and work anniversaries."

    def handle(self, *args, **options):
        """Send a reminder about birthdays and work anniversaries."""

        MONTHS_PER_YEAR = 12
        MONTHS_HALF_YEAR = 6
        today = datetime.date.today()
        users = models.User.objects.all()
        users_born_this_month = []
        users_work_anniversary = {}
        for user in users:
            if (
                user.is_active
                and user.userinfo.birth_date
                and user.userinfo.birth_date.month == today.month
            ):
                users_born_this_month.append(user)
            users_born_this_month.sort(key=lambda x: x.userinfo.birth_date.day)

            if user.is_active and user.date_joined:
                if (
                    user.date_joined.month + MONTHS_HALF_YEAR
                ) % MONTHS_PER_YEAR == today.month:
                    users_work_anniversary.setdefault("0.5", [])
                    users_work_anniversary["0.5"].append(user)
                if user.date_joined.month == today.month:
                    years = today.year - user.date_joined.year
                    if years:
                        users_work_anniversary.setdefault(str(years), [])
                        users_work_anniversary[str(years)].append(user)

        keys_to_sort = list(users_work_anniversary.keys())
        keys_to_sort.sort(reverse=True)
        users_work_anniversary = {i: users_work_anniversary[i] for i in keys_to_sort}

        if users_born_this_month or users_work_anniversary:
            recipients = get_users_with_permission(
                models.PERMISSION_RECEIVE_BDAY_ANNIVERSARY_REMINDER
            )

            for recipient in recipients:
                if recipient.email:
                    log.info(f"Sending reminder to {recipient.email}")

                    send_mail(
                        recipient.email,
                        _("Colleague's birthday and work anniversary reminder"),
                        "ninetofiver/emails/b_day_and_anniversary_reminder.pug",
                        context={
                            "recipient": recipient,
                            "users_born_this_month": users_born_this_month,
                            "users_work_anniversary": users_work_anniversary,
                        },
                    )
