from django.db import models
from django.utils.text import slugify
from django.contrib import messages
from django.shortcuts import render, redirect
from wagtail.admin.panels import FieldPanel, InlinePanel
from modelcluster.fields import ParentalKey
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import (
    FieldPanel, FieldRowPanel,
    InlinePanel, MultiFieldPanel
)
from wagtail.fields import RichTextField
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from django.core.validators import RegexValidator


class FormField(AbstractFormField):
    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='custom_form_fields')

    regex_validator = models.CharField(
        max_length=255,
        blank=True,
        help_text="Enter a regular expression for custom validation (do not apply to checkbox, dropdowns, multiple select, radio buttons, and hidden field)"
    )

    panels = [
        FieldPanel("label"), 
        FieldPanel("field_type"), 
        FieldPanel("required"), 
        FieldPanel("choices"), 
        FieldPanel("default_value"), 
        FieldPanel("help_text"), 
        FieldPanel("regex_validator")
    ]


class FormPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro'),
        InlinePanel('custom_form_fields', label="Form fields"),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]

    template = "form/form_page.html"

    def get_form_fields(self):
        return self.custom_form_fields.all()
    
    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        
        form_fields = {field.label: field for field in self.custom_form_fields.all()}

        # Force `get_form_field()` to apply attributes
        for field_name, field in form.fields.items():

            form_field = form_fields.get(field.label)  # Fetch stored model field

            # Apply regex validation if `regex_validator` is set
            if form_field and hasattr(form_field, "regex_validator") and form_field.regex_validator:
                print("apply regex validator to: ", field_name)
                field.validators.append(RegexValidator(
                    regex=form_field.regex_validator,
                    message=f"Input must match pattern."
                ))
                

            if hasattr(field, 'widget'):
                widget_type = field.widget.__class__.__name__  # Get the widget class name
                # Apply Bootstrap classes dynamically
                if widget_type in ["TextInput", "EmailInput", "NumberInput", "URLInput"]:
                    field.widget.attrs.update({"class": "form-control"})
                elif widget_type in ["Textarea"]:
                    field.widget.attrs.update({"class": "form-control text-area"})
                elif widget_type in ["CheckboxInput"]:
                    field.widget.attrs.update({"class": "form-check-input"})
                elif widget_type in ["Select"]:
                    field.widget.attrs.update({"class": "form-select"})
                else:
                    field.widget.attrs.update({"class": "form-control"})  # Default

        return form 

    def serve(self, request, *args, **kwargs):
        """Override the default Wagtail form processing."""
        form = self.get_form(request.POST or None)

        if request.method == "POST":
            if form.is_valid():
                print("Form is valid! Saving...")
                messages.success(request, "Submission Successful!")
                self.process_form_submission(form)
                return redirect(self.url)  # Save submission only if valid
            else:
                print("Form validation failed! Errors:", form.errors)
                return render(request, "form/form_page.html", {"page": self, "form": form})

        return super().serve(request, *args, **kwargs)
