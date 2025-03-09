from django.contrib import admin
from django.utils.safestring import mark_safe
import json
from .models import FormPageSubmission


@admin.register(FormPageSubmission)
class FormPageSubmissionAdmin(admin.ModelAdmin):
    list_display = ("id", "form_page", "submit_time", "short_form_data")
    search_fields = ("form_data",)
    ordering = ("-submit_time",)
    
    def short_form_data(self, obj):
        """Show a short preview of the submission data"""
        data = json.dumps(obj.form_data, indent=2)
        return mark_safe(f'<pre style="white-space: pre-wrap;">{data[:300]}...</pre>')

    short_form_data.short_description = "Submission Data"
