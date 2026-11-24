from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'users'
        managed = False
        
class UserProfile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, db_column='user_id')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    bio = models.TextField()
    phone = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    profile_image = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'user_profiles'
        managed = False
        
class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_column='user_id')
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    technologies = models.TextField(null=True, blank=True)
    project_url = models.TextField("Live link", null=True, blank=True)
    github_url = models.TextField("GitHub repo", null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'projects'
        managed = False
        
class ProjectMedia(models.Model):
    media_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, db_column='project_id')
    media_type = models.CharField(max_length=255, null=True, blank=True)
    media_url = models.TextField()
    caption = models.TextField(null=True, blank=True)
    display_order = models.IntegerField(null=True, blank=True)
    uploaded_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'project_media'
        managed = False
        
class Skill(models.Model):
    SKILL_TYPES = (
        ("technical", "Technical skill"),
        ("soft", "Soft skill"),
    )

    skill_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_column='user_id')
    skill_type = models.CharField(max_length=20, choices=SKILL_TYPES, default="technical")
    skill_name = models.CharField(max_length=255)
    category = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    proficiency_level = models.CharField(max_length=255, null=True, blank=True)
    is_featured = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'skills'
        managed = False

class SocialLink(models.Model):
    social_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_column='user_id')
    platform = models.CharField(max_length=255)
    username = models.CharField(max_length=255, null=True, blank=True)
    profile_url = models.TextField()
    display_order = models.IntegerField(null=True, blank=True)
    is_visible = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'social_links'
        managed = False
        
class Achievement(models.Model):
    achievement_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_column='user_id')
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    organization = models.CharField(max_length=255, null=True, blank=True)
    achievement_date = models.DateField(null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    image_url = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'achievements'
        managed = False

class Certificate(models.Model):
    certificate_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_column='user_id')
    certificate_name = models.CharField(max_length=255)
    issuing_organization = models.CharField(max_length=150, null=True, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    certificate_url = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'certificate'
        managed = False

class EducationalBackground(models.Model):
    educational_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_column='user_id')
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=255, null=True, blank=True)
    field_of_study = models.CharField(max_length=255, null=True, blank=True)
    # years only, as text: "2022", "2026", "Present"
    start_date = models.CharField("Start year", max_length=20, null=True, blank=True)
    end_date = models.CharField("End year", max_length=20, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'educational_background'
        managed = False


class Experience(models.Model):
    experience_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_column='user_id')
    position = models.CharField(max_length=255)
    company = models.CharField(max_length=255, null=True, blank=True)
    employment_type = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'experience'
        managed = False
        
class ContactMessage(models.Model):
    message_id = models.AutoField(primary_key=True)
    profile = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, db_column='profile_id')
    sender_name = models.CharField(max_length=255)
    sender_email = models.CharField(max_length=255)
    subject = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=255, null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'contact_messages'
        managed = False


class Analytics(models.Model):
    analytics_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, db_column='project_id')
    page_visited = models.CharField(max_length=255)
    referrer = models.TextField(null=True, blank=True)
    interaction_type = models.CharField(max_length=255, null=True, blank=True)
    interaction_count = models.IntegerField(null=True, blank=True)
    is_unique = models.BooleanField(null=True, blank=True)
    visited_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'analytics'
        managed = False