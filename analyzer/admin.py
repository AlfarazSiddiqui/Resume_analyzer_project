from django.contrib import admin
from .models import Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('original_filename', 'user', 'overall_score', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('original_filename', 'user__username')
    readonly_fields = ('parsed_text', 'skills_found', 'matched_skills', 'missing_skills', 'suggestions')
