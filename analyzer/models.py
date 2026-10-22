from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


def resume_upload_path(instance, filename):
    return f'resumes/user_{instance.user.id}/{filename}'


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    file = models.FileField(
        upload_to=resume_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'txt'])],
    )
    original_filename = models.CharField(max_length=255, blank=True)
    job_description = models.TextField(blank=True)
    parsed_text = models.TextField(blank=True)

    overall_score = models.FloatField(default=0)
    keyword_score = models.FloatField(default=0)
    section_score = models.FloatField(default=0)
    contact_score = models.FloatField(default=0)
    readability_score = models.FloatField(default=0)

    sections = models.JSONField(default=dict, blank=True)
    skills_found = models.JSONField(default=list, blank=True)
    matched_skills = models.JSONField(default=list, blank=True)
    missing_skills = models.JSONField(default=list, blank=True)
    suggestions = models.JSONField(default=list, blank=True)
    word_count = models.IntegerField(default=0)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.original_filename or self.file.name} — {self.user.username} ({self.overall_score}%)"

    @property
    def score_grade(self):
        if self.overall_score >= 80:
            return 'Excellent'
        elif self.overall_score >= 60:
            return 'Good'
        elif self.overall_score >= 40:
            return 'Fair'
        return 'Needs Work'
