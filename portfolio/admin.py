from django import forms
from django.contrib import admin
from django.utils import timezone

from .models import (
    Achievement,
    Analytics,
    Certificate,
    ContactMessage,
    EducationalBackground,
    Experience,
    Project,
    ProjectMedia,
    Skill,
    SocialLink,
    User,
    UserProfile,
)

# Readable names in dropdowns ("xaixai" instead of "User object (1)").
# Done here so models.py stays untouched.
User.__str__ = lambda self: self.username
UserProfile.__str__ = lambda self: f"{self.first_name} {self.last_name}".strip()
Project.__str__ = lambda self: self.title


admin.site.site_header = "xynexkyym · Portfolio Admin"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Manage your beach portfolio"


class CreatedAtMixin:
    """Fills created_at on new rows (the tables don't set it themselves)."""

    def save_model(self, request, obj, form, change):
        if hasattr(obj, "created_at") and not obj.created_at:
            obj.created_at = timezone.now()
        super().save_model(request, obj, form, change)


# account

@admin.register(User)
class PortfolioUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "status", "created_at")
    search_fields = ("username", "email")
    readonly_fields = ("password_hash", "created_at", "updated_at")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "user", "location", "phone")
    search_fields = ("first_name", "last_name", "bio")


class SocialLinkForm(forms.ModelForm):
    # a plain ticked checkbox instead of the Yes / No / Unknown dropdown,
    # so a new link is visible on the site unless you untick it
    is_visible = forms.BooleanField(required=False, initial=True, label="Visible on site")

    class Meta:
        model = SocialLink
        fields = "__all__"
        help_texts = {
            "platform": 'Use "LinkedIn" or "GitHub" so the site shows the right icon.',
            "profile_url": "Full link, starting with https://",
        }


@admin.register(SocialLink)
class SocialLinkAdmin(CreatedAtMixin, admin.ModelAdmin):
    form = SocialLinkForm
    list_display = ("platform", "username", "profile_url", "display_order", "is_visible")
    list_editable = ("display_order", "is_visible")
    list_filter = ("platform", "is_visible")
    search_fields = ("platform", "username", "profile_url")
    ordering = ("display_order", "platform")
    fields = ("user", "platform", "username", "profile_url", "display_order", "is_visible")


# projects

class ProjectMediaInline(admin.TabularInline):
    model = ProjectMedia
    extra = 1
    fields = ("media_type", "media_url", "caption", "display_order")


@admin.register(Project)
class ProjectAdmin(CreatedAtMixin, admin.ModelAdmin):
    list_display = ("title", "category", "technologies", "created_at")
    list_filter = ("category",)
    search_fields = ("title", "description", "technologies")
    inlines = (ProjectMediaInline,)
    exclude = ("created_at",)


@admin.register(ProjectMedia)
class ProjectMediaAdmin(admin.ModelAdmin):
    list_display = ("project", "media_type", "caption", "display_order")
    list_filter = ("media_type",)
    ordering = ("project", "display_order")


# skills & history

@admin.register(Skill)
class SkillAdmin(CreatedAtMixin, admin.ModelAdmin):
    list_display = ("skill_name", "category", "proficiency_level", "is_featured")
    list_editable = ("proficiency_level", "is_featured")
    list_filter = ("category", "proficiency_level", "is_featured")
    search_fields = ("skill_name", "description")
    ordering = ("category", "skill_name")
    exclude = ("created_at",)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("position", "company", "employment_type", "start_date", "end_date")
    list_filter = ("employment_type",)
    search_fields = ("position", "company")
    ordering = ("-start_date",)


@admin.register(EducationalBackground)
class EducationalBackgroundAdmin(admin.ModelAdmin):
    list_display = ("degree", "field_of_study", "institution", "start_date", "end_date")
    search_fields = ("degree", "institution", "field_of_study")
    ordering = ("-start_date",)


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("certificate_name", "issuing_organization", "issue_date")
    search_fields = ("certificate_name", "issuing_organization")
    ordering = ("-issue_date",)


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ("title", "organization", "category", "achievement_date")
    list_filter = ("category",)
    search_fields = ("title", "organization")
    ordering = ("-achievement_date",)


# inbox & stats (read-only)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("sender_name", "sender_email", "subject", "status", "sent_at")
    list_filter = ("status",)
    search_fields = ("sender_name", "sender_email", "subject", "message")
    ordering = ("-sent_at",)
    readonly_fields = ("profile", "sender_name", "sender_email", "subject", "message", "sent_at")


@admin.register(Analytics)
class AnalyticsAdmin(admin.ModelAdmin):
    list_display = ("page_visited", "project", "interaction_type", "interaction_count", "is_unique", "visited_at")
    list_filter = ("interaction_type", "is_unique")
    ordering = ("-visited_at",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False