"""
python manage.py upgrade_db

Applies the small database changes the newer code needs. Your portfolio
tables are managed by hand (managed = False), so Django's `migrate` can't do
this for you. Every step checks first, so running it again is always safe.

  1. Education start/end: full dates -> year-only text ("2022", "Present")
  2. Skills: new "skill_type" column (technical / soft), existing skills = technical
  3. Projects: new "github_url" column for each project's repo link
"""

from django.core.management.base import BaseCommand
from django.db import connection, transaction


def column_types(cursor, table):
    cursor.execute(
        """
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = current_schema() AND table_name = %s
        """,
        [table],
    )
    return dict(cursor.fetchall())


class Command(BaseCommand):
    help = "Apply the portfolio's database changes (safe to run more than once)."

    def handle(self, *args, **options):
        with transaction.atomic(), connection.cursor() as cursor:

            # 1. education years
            edu = column_types(cursor, "educational_background")
            for col in ("start_date", "end_date"):
                if edu.get(col) == "date":
                    cursor.execute(
                        f'ALTER TABLE educational_background ALTER COLUMN "{col}" '
                        f"TYPE varchar(20) USING to_char(\"{col}\", 'YYYY')"
                    )
                    self.stdout.write(self.style.SUCCESS(f"  Education {col}: now year-only"))
                else:
                    self.stdout.write(f"  Education {col}: already year-only")

            # 2. skill type
            skills = column_types(cursor, "skills")
            if "skill_type" not in skills:
                cursor.execute(
                    "ALTER TABLE skills ADD COLUMN skill_type varchar(20) "
                    "NOT NULL DEFAULT 'technical'"
                )
                self.stdout.write(self.style.SUCCESS("  Skills: added Technical / Soft type"))
            else:
                self.stdout.write("  Skills: type column already there")

            # 3. project GitHub link
            projects = column_types(cursor, "projects")
            if "github_url" not in projects:
                cursor.execute("ALTER TABLE projects ADD COLUMN github_url text")
                self.stdout.write(self.style.SUCCESS("  Projects: added GitHub repo link"))
            else:
                self.stdout.write("  Projects: GitHub link column already there")

        self.stdout.write(self.style.SUCCESS("Database is up to date."))
