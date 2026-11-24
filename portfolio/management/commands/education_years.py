"""
python manage.py education_years

One-time change: turns educational_background.start_date / end_date from
full dates (2022-06-01) into short text that holds just the year ("2022",
"Present"). Existing rows keep their year. Safe to run twice: it does nothing
if the columns are already text.
"""

from django.core.management.base import BaseCommand
from django.db import connection, transaction

COLUMNS = ("start_date", "end_date")


class Command(BaseCommand):
    help = "Change Education start/end dates to year-only text (one time)."

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_schema = current_schema()
                  AND table_name = 'educational_background'
                  AND column_name IN ('start_date', 'end_date')
                """
            )
            types = dict(cursor.fetchall())

        if not types:
            self.stderr.write("Table educational_background was not found. Nothing changed.")
            return

        to_change = [col for col in COLUMNS if types.get(col) == "date"]
        if not to_change:
            self.stdout.write(self.style.SUCCESS("Already year-only text. Nothing to do."))
            return

        with transaction.atomic(), connection.cursor() as cursor:
            for col in to_change:
                cursor.execute(
                    f'ALTER TABLE educational_background '
                    f'ALTER COLUMN "{col}" TYPE varchar(20) '
                    f"USING to_char(\"{col}\", 'YYYY')"
                )
                self.stdout.write(self.style.SUCCESS(f"  {col}: date -> year text"))

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT institution, start_date, end_date FROM educational_background ORDER BY educational_id"
            )
            rows = cursor.fetchall()

        self.stdout.write(self.style.SUCCESS("Done. Your education entries now:"))
        for institution, start, end in rows:
            self.stdout.write(f"  {institution}: {start or '—'} – {end or '—'}")
