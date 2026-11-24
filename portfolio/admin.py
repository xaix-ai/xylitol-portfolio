from django import forms
from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .templatetags.portfolio_extras import is_image, media_kind, media_src

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


IMAGE_HELP = (
    "Type a file name from portfolio/static/portfolio/images/ "
    "(e.g. <b>{folder}/my-picture.png</b>), or paste a full https:// image link "
    "or a Google Drive share link (shared as 'Anyone with the link')."
)


def preview(value, kind="image", height=90):
    """Small thumbnail shown inside the admin."""
    if not value:
        return "—"
    src = media_src(value)
    if kind == "video":
        return format_html(
            '<video src="{}" style="height:{}px;border-radius:6px;background:#eee" muted></video>',
            src, height,
        )
    return format_html(
        '<a href="{0}" target="_blank" rel="noopener">'
        '<img src="{0}" style="height:{1}px;max-width:220px;object-fit:cover;'
        'border-radius:6px;background:#eee" alt=""></a>',
        src, height,
    )


# account

@admin.register(User)
class PortfolioUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "status", "created_at")
    search_fields = ("username", "email")
    readonly_fields = ("password_hash", "created_at", "updated_at")


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = "__all__"
        widgets = {
            "profile_image": forms.TextInput(attrs={"size": 70}),
        }
        help_texts = {
            "profile_image": IMAGE_HELP.format(folder="profile"),
            "bio": "Shown in About. 2–4 sentences about who you are and what you like working on.",
            "phone": "Private: kept here for you only, never shown on the site.",
            "user": "Pick the portfolio user whose projects, skills and links should appear on the site.",
        }


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    form = UserProfileForm
    list_display = ("first_name", "last_name", "user", "location", "phone", "photo")
    search_fields = ("first_name", "last_name", "bio")
    readonly_fields = ("photo_preview",)

    @admin.display(description="Photo")
    def photo(self, obj):
        return preview(obj.profile_image, height=40)

    @admin.display(description="Photo preview")
    def photo_preview(self, obj):
        return preview(obj.profile_image, height=140)


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

MEDIA_TYPES = (
    ("image", "Screenshot / image"),
    ("video", "Screen recording (mp4 / webm)"),
)


class ProjectMediaForm(forms.ModelForm):
    media_type = forms.ChoiceField(choices=MEDIA_TYPES, initial="image")

    class Meta:
        model = ProjectMedia
        fields = "__all__"
        widgets = {
            "media_url": forms.TextInput(attrs={"size": 50}),
            "caption": forms.TextInput(attrs={"size": 40}),
        }
        help_texts = {
            "media_url": IMAGE_HELP.format(folder="projects"),
            "caption": "Optional. Shown under the screenshot, e.g. \"Dashboard home page\".",
            "display_order": "1 shows first.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # older rows may say "Image" / "screenshot": map them onto the dropdown
        current = (self.initial.get("media_type") or "").lower()
        self.initial["media_type"] = "video" if "video" in current else "image"


class ProjectMediaInline(admin.TabularInline):
    model = ProjectMedia
    form = ProjectMediaForm
    extra = 1
    fields = ("thumbnail", "media_type", "media_url", "caption", "display_order")
    readonly_fields = ("thumbnail",)
    ordering = ("display_order",)
    verbose_name = "Screenshot / recording"
    verbose_name_plural = "Project interface (screenshots shown in the browser window on the site)"

    @admin.display(description="Preview")
    def thumbnail(self, obj):
        if not obj or not obj.media_url:
            return "—"
        return preview(obj.media_url, kind=media_kind(obj), height=60)


PROJECT_CATEGORIES = (
    "Web Development",
    "Database Management",
    "Data Analysis",
    "Data Visualization",
    "Data Cleaning",
    "Machine Learning",
    "Mobile App",
    "UI/UX Design",
    "Automation",
)


SKILL_CATEGORIES = (
    "Web Development",
    "Database Management",
    "Data Analysis",
    "Data Visualization",
    "Programming Languages",
    "Tools & Software",
    "Machine Learning",
    "UI/UX Design",
    "Version Control",
    "Cloud & Deployment",
)


class CategoryInput(forms.TextInput):
    """A text box with suggestions: pick one, or type your own."""

    def __init__(self, options, attrs=None):
        super().__init__(attrs)
        self.options = options

    def render(self, name, value, attrs=None, renderer=None):
        list_id = f"{name}-suggestions"
        attrs = {**(attrs or {}), "list": list_id, "autocomplete": "off"}
        box = super().render(name, value, attrs, renderer)
        options = "".join(format_html('<option value="{}">', option) for option in self.options)
        return format_html('{}<datalist id="{}">{}</datalist>', box, list_id, mark_safe(options))


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = "__all__"
        widgets = {
            "category": CategoryInput(PROJECT_CATEGORIES, attrs={"size": 40}),
            "project_url": forms.TextInput(attrs={"size": 70}),
            "github_url": forms.TextInput(attrs={"size": 70}),
            "technologies": forms.TextInput(attrs={"size": 70}),
        }
        help_texts = {
            "category": "What kind of project: click the box to pick (Web Development, "
                        "Database Management, Data Analysis...) or type your own. "
                        "Visitors can filter projects by this.",
            "description": "2–3 sentences: the problem, what you built, and the result. "
                           "Lines starting with - become bullets.",
            "technologies": "Comma-separated, e.g. Python, Pandas, SQL, Power BI. Each one becomes a chip.",
            "project_url": "Optional. The live website or published dashboard (https://...). "
                           "Shows a 'Live Demo' button.",
            "github_url": "Optional. This project's GitHub repository, "
                          "e.g. https://github.com/xaix-ai/sales-dashboard. Shows a 'Code' button.",
        }


@admin.register(Project)
class ProjectAdmin(CreatedAtMixin, admin.ModelAdmin):
    form = ProjectForm
    list_display = ("title", "cover", "category", "technologies", "has_github", "created_at")
    list_filter = ("category",)
    search_fields = ("title", "description", "technologies")
    inlines = (ProjectMediaInline,)
    exclude = ("created_at",)

    @admin.display(description="GitHub", boolean=True)
    def has_github(self, obj):
        return bool(obj.github_url)

    @admin.display(description="Cover")
    def cover(self, obj):
        first = obj.projectmedia_set.order_by("display_order").first()
        if not first:
            return "—"
        return preview(first.media_url, kind=media_kind(first), height=40)

    def save_formset(self, request, form, formset, change):
        # stamp new screenshots with the upload time
        for media in formset.save(commit=False):
            if not media.uploaded_at:
                media.uploaded_at = timezone.now()
            media.save()
        for media in formset.deleted_objects:
            media.delete()
        formset.save_m2m()


@admin.register(ProjectMedia)
class ProjectMediaAdmin(admin.ModelAdmin):
    form = ProjectMediaForm
    list_display = ("project", "thumbnail", "media_type", "caption", "display_order")

    @admin.display(description="Preview")
    def thumbnail(self, obj):
        return preview(obj.media_url, kind=media_kind(obj), height=40)

    list_filter = ("media_type",)
    ordering = ("project", "display_order")


# skills & history

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = "__all__"
        widgets = {
            "skill_type": forms.RadioSelect,
            "category": CategoryInput(SKILL_CATEGORIES, attrs={"size": 40}),
        }
        help_texts = {
            "skill_type": "Technical = tools and know-how (SQL, Excel, Python). "
                          "Soft = people skills (Communication, Teamwork).",
            "category": "Technical only: what the skill is for. Click the box to pick "
                        "(Web Development, Database Management, Data Analysis...) or type your own. "
                        "Skills with the same category are grouped together. Leave empty for soft skills.",
            "proficiency_level": "Technical only, e.g. Beginner, Intermediate, Advanced. "
                                 "Leave empty for soft skills.",
            "description": "Optional. One short line, or bullets starting with - ",
        }


@admin.register(Skill)
class SkillAdmin(CreatedAtMixin, admin.ModelAdmin):
    form = SkillForm
    list_display = ("skill_name", "skill_type", "category", "proficiency_level", "is_featured")
    list_editable = ("proficiency_level", "is_featured")
    list_filter = ("skill_type", "category", "proficiency_level", "is_featured")
    fieldsets = (
        (None, {"fields": ("user", "skill_type", "skill_name", "description")}),
        ("Technical skill details (leave empty for soft skills)", {
            "fields": ("category", "proficiency_level", "is_featured"),
        }),
    )
    search_fields = ("skill_name", "description")
    ordering = ("skill_type", "category", "skill_name")


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("position", "company", "employment_type", "start_date", "end_date")
    list_filter = ("employment_type",)
    search_fields = ("position", "company")
    ordering = ("-start_date",)


class EducationalBackgroundForm(forms.ModelForm):
    class Meta:
        model = EducationalBackground
        fields = "__all__"
        labels = {"field_of_study": "Field of study / Strand"}
        widgets = {
            "start_date": forms.TextInput(attrs={"size": 10, "placeholder": "2022"}),
            "end_date": forms.TextInput(attrs={"size": 10, "placeholder": "2026 or Present"}),
        }
        help_texts = {
            "degree": "College and up only, e.g. BS Information Technology. "
                      "Leave EMPTY for Junior / Senior High School: the school name becomes the title.",
            "field_of_study": "Optional. For senior high, the strand, e.g. STEM.",
            "start_date": "Year only, e.g. 2022.",
            "end_date": "Year only, e.g. 2026. Type Present if you're still studying there.",
        }

    def _clean_year(self, field):
        value = (self.cleaned_data.get(field) or "").strip()
        if not value:
            return None
        if value.lower() in ("present", "current", "now"):
            return "Present"
        if not (value.isdigit() and len(value) == 4):
            raise forms.ValidationError("Type a 4-digit year like 2024, or Present.")
        return value

    def clean_start_date(self):
        return self._clean_year("start_date")

    def clean_end_date(self):
        return self._clean_year("end_date")


@admin.register(EducationalBackground)
class EducationalBackgroundAdmin(admin.ModelAdmin):
    form = EducationalBackgroundForm
    list_display = ("degree", "field_of_study", "institution", "start_date", "end_date")
    search_fields = ("degree", "institution", "field_of_study")
    ordering = ("-start_date",)


class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = "__all__"
        widgets = {"certificate_url": forms.TextInput(attrs={"size": 70})}
        help_texts = {
            "certificate_url": "A picture of the certificate shows a preview on the site: "
                               + IMAGE_HELP.format(folder="certificates")
                               + " Any other link (e.g. a Coursera verify page or PDF) shows a "
                                 "'View Certificate' button only.",
        }


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    form = CertificateForm
    list_display = ("certificate_name", "thumbnail", "issuing_organization", "issue_date")
    search_fields = ("certificate_name", "issuing_organization")
    ordering = ("-issue_date",)
    readonly_fields = ("certificate_preview",)

    @admin.display(description="Preview")
    def thumbnail(self, obj):
        return preview(obj.certificate_url, height=40) if is_image(obj.certificate_url) else "—"

    @admin.display(description="Preview")
    def certificate_preview(self, obj):
        return preview(obj.certificate_url, height=160) if is_image(obj.certificate_url) else "—"


class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = "__all__"
        widgets = {"image_url": forms.TextInput(attrs={"size": 70})}
        help_texts = {"image_url": "Optional photo. " + IMAGE_HELP.format(folder="achievements")}


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    form = AchievementForm
    list_display = ("title", "thumbnail", "organization", "category", "achievement_date")
    list_filter = ("category",)
    search_fields = ("title", "organization")
    ordering = ("-achievement_date",)
    readonly_fields = ("photo_preview",)

    @admin.display(description="Photo")
    def thumbnail(self, obj):
        return preview(obj.image_url, height=40)

    @admin.display(description="Photo preview")
    def photo_preview(self, obj):
        return preview(obj.image_url, height=160)


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