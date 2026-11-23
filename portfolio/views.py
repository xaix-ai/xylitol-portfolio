from django.db.models import F, Prefetch, Q
from django.shortcuts import render

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

        skills = Skill.objects.filter(user=user).order_by("category", "skill_name")

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
        skills = Skill.objects.none()
        experiences = Experience.objects.none()
        education = EducationalBackground.objects.none()
        certificates = Certificate.objects.none()
        achievements = Achievement.objects.none()
        social_links = SocialLink.objects.none()

    contact = {
        "email": user.email if user else "",
        "phone": profile.phone if profile else "",
        "location": profile.location if profile else "",
        "social_links": social_links,
    }

    context = {
        "profile": profile,
        "projects": projects,
        "skills": skills,
        "experiences": experiences,
        "education": education,
        "certificates": certificates,
        "achievements": achievements,
        "contact": contact,
    }

    return render(request, "portfolio/home.html", context)
