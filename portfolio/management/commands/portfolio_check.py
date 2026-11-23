"""
python manage.py portfolio_check

Explains, in plain words, what the home page will show and why something
might be missing (wrong user picked, link hidden, image file not found...).
It only READS the database; it never changes anything.
"""

from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from portfolio.models import (
    Achievement,
    Certificate,
    EducationalBackground,
    Experience,
    Project,
    ProjectMedia,
    Skill,
    SocialLink,
    User,
    UserProfile,
)
from portfolio.templatetags.portfolio_extras import media_kind
from portfolio.views import get_portfolio_owner

IMAGES_DIR = Path(settings.BASE_DIR) / "portfolio" / "static" / "portfolio" / "images"


def _local_image_problem(value):
    """Return a message if a typed image path points at a file that isn't there."""
    value = (value or "").strip()
    if not value or "://" in value or value.startswith(("/", "data:")):
        return None
    clean = value.removeprefix("./").removeprefix("images/")
    if not (IMAGES_DIR / clean).is_file():
        return f'file not found: portfolio/static/portfolio/images/{clean}'
    return None


class Command(BaseCommand):
    help = "Check what the portfolio home page will show, and why something might be missing."

    def ok(self, text):
        self.stdout.write(self.style.SUCCESS("  OK    ") + text)

    def warn(self, text):
        self.stdout.write(self.style.WARNING("  !!    ") + text)

    def info(self, text):
        self.stdout.write("        " + text)

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("\n1. Who the site is about"))

        users = list(User.objects.order_by("user_id"))
        profiles = list(UserProfile.objects.select_related("user").order_by("profile_id"))
        profile, owner = get_portfolio_owner()

        if not users:
            self.warn("There are no portfolio users yet.")
            self.info("Admin -> Portfolio -> Users -> Add user, then make a User profile for it.")
            return

        for u in users:
            self.info(f"Portfolio user #{u.user_id}: {u.username} <{u.email}>")

        if not profiles:
            self.warn("No User profile exists, so About/phone/location are empty.")
            self.info("Admin -> Portfolio -> User profiles -> Add, and pick your user.")
        elif len(profiles) > 1:
            self.warn(f"There are {len(profiles)} profiles. The site only uses the FIRST one:")
            for p in profiles:
                self.info(f"  profile #{p.profile_id} -> user {p.user.username}")
            self.info("Delete the extra profile(s) you don't need.")
        else:
            self.ok(f"One profile: {profile.first_name} {profile.last_name}")

        self.ok(f"The site shows content that belongs to user: {owner.username} (#{owner.user_id})")

        # ---- per section --------------------------------------------------
        self.stdout.write(self.style.MIGRATE_HEADING("\n2. What each section will show"))

        sections = [
            ("Projects", Project),
            ("Skills", Skill),
            ("Experience", Experience),
            ("Education", EducationalBackground),
            ("Certificates", Certificate),
            ("Achievements", Achievement),
            ("Social links", SocialLink),
        ]

        for label, model in sections:
            mine = model.objects.filter(user=owner).count()
            others = model.objects.exclude(user=owner).count()
            if mine:
                self.ok(f"{label}: {mine}")
            else:
                self.warn(f"{label}: nothing yet")
            if others:
                self.warn(
                    f"{label}: {others} more saved under a DIFFERENT user, so they are hidden. "
                    f"Open each one in the admin and set User to '{owner.username}'."
                )

        # ---- social links ---------------------------------------------------
        self.stdout.write(self.style.MIGRATE_HEADING("\n3. Social links (Contact -> Find me online)"))
        links = SocialLink.objects.select_related("user").order_by("social_id")
        if not links:
            self.warn("No social links saved at all. Admin -> Portfolio -> Social links -> Add.")
        for link in links:
            problems = []
            if link.user_id != owner.user_id:
                problems.append(f"belongs to user '{link.user.username}', not '{owner.username}'")
            if link.is_visible is False:
                problems.append('"Visible on site" is unticked')
            if not (link.profile_url or "").startswith(("https://", "http://", "mailto:")):
                problems.append("URL should start with https://")
            name = f"{link.platform} -> {link.profile_url}"
            if problems:
                self.warn(name + "   (" + "; ".join(problems) + ")")
            else:
                self.ok(name)

        # ---- images ---------------------------------------------------------
        self.stdout.write(self.style.MIGRATE_HEADING("\n4. Images"))
        found_problem = False

        if profile:
            if not profile.profile_image:
                self.warn("Profile photo: empty (About shows text only)")
            else:
                problem = _local_image_problem(profile.profile_image)
                if problem:
                    found_problem = True
                    self.warn(f"Profile photo: {problem}")
                else:
                    self.ok("Profile photo set")

        for project in Project.objects.filter(user=owner).order_by("project_id"):
            media = list(ProjectMedia.objects.filter(project=project))
            if not media:
                self.warn(f'Project "{project.title}": no screenshots yet (shows "preview coming soon")')
                continue
            kinds = [media_kind(m) for m in media]
            self.ok(f'Project "{project.title}": {kinds.count("image")} image(s), {kinds.count("video")} video(s)')
            for m in media:
                problem = _local_image_problem(m.media_url)
                if problem:
                    found_problem = True
                    self.warn(f"    {problem}")

        for item in Achievement.objects.filter(user=owner).exclude(image_url__isnull=True).exclude(image_url=""):
            problem = _local_image_problem(item.image_url)
            if problem:
                found_problem = True
                self.warn(f'Achievement "{item.title}": {problem}')

        for item in Certificate.objects.filter(user=owner).exclude(certificate_url__isnull=True).exclude(certificate_url=""):
            problem = _local_image_problem(item.certificate_url)
            if problem:
                found_problem = True
                self.warn(f'Certificate "{item.certificate_name}": {problem}')

        if not found_problem:
            self.ok("No missing image files found")

        self.stdout.write("")
