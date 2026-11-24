from django.conf import settings
from django.db.models import F, Prefetch, Q
from django.shortcuts import render

from .templatetags.portfolio_extras import slug_key
from .models import (
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


def get_portfolio_owner():
    """
    The site shows ONE person: the user linked to the first profile.
    If no profile has been made yet, fall back to the first portfolio user,
    so projects, skills and social links still appear.
    """
    profile = (
        UserProfile.objects
        .select_related("user")
        .order_by("profile_id")
        .first()
    )
    if profile:
        return profile, profile.user

    return None, User.objects.order_by("user_id").first()


def home(request):

    profile, user = get_portfolio_owner()

    if user:
        projects = (
            Project.objects
            .filter(user=user)
            .prefetch_related(
                Prefetch(
                    "projectmedia_set",
                    queryset=ProjectMedia.objects.order_by(
                        F("display_order").asc(nulls_last=True), "media_id"
                    ),
                )
            )
            .order_by(F("created_at").desc(nulls_last=True), "-project_id")
        )

        skills = Skill.objects.filter(user=user)
        # anything not marked "soft" counts as technical (older rows have no type)
        # project types for the filter buttons (only shown with 2+ types)
        counts = {}
        for name in projects.values_list("category", flat=True):
            name = (name or "").strip()
            if name:
                counts[name] = counts.get(name, 0) + 1
        project_categories = [
            {"name": name, "key": slug_key(name), "count": count}
            for name, count in sorted(counts.items())
        ] if len(counts) > 1 else []

        technical_skills = skills.exclude(skill_type="soft").order_by(
            F("category").asc(nulls_last=True), "skill_name"
        )
        soft_skills = skills.filter(skill_type="soft").order_by("skill_id")

        experiences = (
            Experience.objects
            .filter(user=user)
            .order_by(F("start_date").desc(nulls_last=True))
        )

        education = (
            EducationalBackground.objects
            .filter(user=user)
            .order_by(F("end_date").desc(nulls_first=True), F("start_date").desc(nulls_last=True))
        )

        certificates = (
            Certificate.objects
            .filter(user=user)
            .order_by(F("issue_date").desc(nulls_last=True))
        )

        achievements = (
            Achievement.objects
            .filter(user=user)
            .order_by(F("achievement_date").desc(nulls_last=True))
        )

        # A link counts as visible unless it was explicitly unticked
        # (rows added outside the admin can have an empty value).
        social_links = (
            SocialLink.objects
            .filter(user=user)
            .filter(Q(is_visible=True) | Q(is_visible__isnull=True))
            .order_by(F("display_order").asc(nulls_last=True), "social_id")
        )
    else:
        projects = Project.objects.none()
        project_categories = []
        technical_skills = Skill.objects.none()
        soft_skills = Skill.objects.none()
        experiences = Experience.objects.none()
        education = EducationalBackground.objects.none()
        certificates = Certificate.objects.none()
        achievements = Achievement.objects.none()
        social_links = SocialLink.objects.none()

    contact = {
        "email": user.email if user else "",
        # phone stays private: it is saved in the admin but never sent to the page
        "location": profile.location if profile else "",
        "social_links": social_links,
    }

    context = {
        "profile": profile,
        "projects": projects,
        "project_categories": project_categories,
        "technical_skills": technical_skills,
        "soft_skills": soft_skills,
        "experiences": experiences,
        "education": education,
        "certificates": certificates,
        "achievements": achievements,
        "contact": contact,
        "cf_analytics_token": "" if settings.DEBUG else settings.CLOUDFLARE_ANALYTICS_TOKEN,
    }

    return render(request, "portfolio/home.html", context)
