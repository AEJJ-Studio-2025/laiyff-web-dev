from django.db import models
from django.core.validators import RegexValidator
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from datetime import datetime


@register_setting
class NavigationSettings(BaseGenericSetting):
    # Address info
    address = RichTextField(blank=True)

    # Contact info
    contact_email = models.TextField(verbose_name="Email", blank=True)
    contact_phone = models.TextField(
        verbose_name="Phone Number",
        blank=True,
        max_length=25,
        help_text="Enter phone number in the format: '+999999999'. Up to 15 digits allowed.",
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ]
    )

    # Social media info
    instagram_url = models.URLField(verbose_name="Instagram Home Page", blank=True)
    facebook_url = models.URLField(verbose_name="Facebook Home Page", blank=True)
    youtube_url = models.URLField(verbose_name="Youtube Home Page", blank=True)
    twitter_url = models.URLField(verbose_name="Twitter Home Page", blank=True)

    # year
    current_year = datetime.now().year

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("address"),
            ],
            heading="Address Information"
        ),
        MultiFieldPanel(
            [
                FieldPanel("contact_email"),
                FieldPanel("contact_phone"),
            ],
            heading="Contact Information"
        ),
        MultiFieldPanel(
            [
                FieldPanel("instagram_url"),
                FieldPanel("facebook_url"),
                FieldPanel("youtube_url"),
                FieldPanel("twitter_url"),
            ],
            heading="Social Media Information"
        )
    ]

    edit_handler = MultiFieldPanel(
        panels,
        heading="Navigation Settings"
    )
