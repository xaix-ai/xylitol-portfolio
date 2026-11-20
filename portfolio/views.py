from django.shortcuts import render
from django.db.models import Prefetch

from .models import (
    UserProfile,
    Project,
    ProjectMedia,
    Skill,
    SocialLink,
    Achievement,
    Certificate,
    EducationalBackground,
    Experience,
)


def home(request):

    # PROFILE
    profile = UserProfile.objects.select_related("user").first()

    if profile:
        user = profile.user
    else:
        user = None


    # PROJECTS
    if user:
        projects = (
            Project.objects
            .filter(user=user)
            .prefetch_related(
                Prefetch(
                    "projectmedia_set",
                    queryset=ProjectMedia.objects.order_by("display_order")
                )
            )
            .order_by("-created_at")
        )
    else:
        projects = Project.objects.none()


    # SKILLS
    if user:
        skills = (
            Skill.objects
            .filter(user=user)
            .order_by("category", "skill_name")
        )
    else:
        skills = Skill.objects.none()


    # EXPERIENCE
    if user:
        experiences = (
            Experience.objects
            .filter(user=user)
            .order_by("-start_date")
        )
    else:
        experiences = Experience.objects.none()


    # EDUCATION
    if user:
        education = (
            EducationalBackground.objects
            .filter(user=user)
            .order_by("-end_date", "-start_date")
        )
    else:
        education = EducationalBackground.objects.none()


    # CERTIFICATES
    if user:
        certificates = (
            Certificate.objects
            .filter(user=user)
            .order_by("-issue_date")
        )
    else:
        certificates = Certificate.objects.none()


    # ACHIEVEMENTS
    if user:
        achievements = (
            Achievement.objects
            .filter(user=user)
            .order_by("-achievement_date")
        )
    else:
        achievements = Achievement.objects.none()


    # SOCIAL LINKS
    if user:
        social_links = (
            SocialLink.objects
            .filter(user=user, is_visible=True)
            .order_by("display_order")
        )
    else:
        social_links = SocialLink.objects.none()


    # CONTACT INFORMATION
    contact = {
        "email": user.email if user else "",
        "phone": profile.phone if profile else "",
        "location": profile.location if profile else "",
        "social_links": social_links,
    }


    # CONTEXT
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