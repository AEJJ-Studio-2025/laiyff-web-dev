from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db import models
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.models import Page, Orderable
from modelcluster.fields import ParentalKey

# Model for form fields
class FormField(Orderable):
    FORM_FIELD_TYPES = [
        ('text', 'Text Field'),
        ('email', 'Email Field'),
        ('number', 'Number Field'),
        ('textarea', 'Text Area'),
    ]

    page = ParentalKey("FormPage", related_name="form_fields", on_delete=models.CASCADE)
    label = models.CharField(max_length=255, help_text="Label for the input field")
    field_type = models.CharField(max_length=20, choices=FORM_FIELD_TYPES, help_text="Type of input field")

    panels = [
        FieldPanel("label"),
        FieldPanel("field_type"),
    ]

    def __str__(self):
        return self.label

# Model for storing form submissions
class FormSubmission(models.Model):
    page = models.ForeignKey("FormPage", on_delete=models.CASCADE, related_name="submissions")
    submitted_at = models.DateTimeField(auto_now_add=True)
    data = models.JSONField()  # Stores the form submission as JSON

    def __str__(self):
        return f"Submission on {self.submitted_at}"

# Main Form Page Model
class FormPage(Page):
    intro_text = models.TextField(blank=True, help_text="Description of the form")

    content_panels = Page.content_panels + [
        FieldPanel('intro_text'),
        InlinePanel('form_fields', label="Form Fields"),
    ]

    def get_form_fields(self):
        """Return all form fields as a list of dictionaries."""
        return [{'label': field.label, 'type': field.field_type} for field in self.form_fields.all()]

    def serve(self, request):
        if request.method == "POST":
            submitted_data = {key: request.POST[key] for key in request.POST if key != "csrfmiddlewaretoken"}
            
            # Save submission in database
            FormSubmission.objects.create(page=self, data=submitted_data)

            # Show success message
            messages.success(request, "Form submitted successfully!")

            return HttpResponseRedirect(self.url)  # Redirect to refresh page after submission

        return render(request, "website/form_page.html", {"page": self})
