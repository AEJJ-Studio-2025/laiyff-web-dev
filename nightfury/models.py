from django.db import models
from django.core.validators import RegexValidator
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.models import Page
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import CharBlock, RichTextBlock, StructBlock, URLBlock, ListBlock
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from datetime import datetime

class NightFuryPage(Page):
    template = "nightfury.html"

    feature_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    excerpt = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    publication_date = models.DateField(blank=True, null=True)
    views_count = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=100, blank=True, null=True)
    tags = models.JSONField(default=list, blank=True, null=True)
    body = RichTextField(blank=True, null=True)

    additional_info = StreamField([
        ("heading", CharBlock(form_classname="full title")),
        ("paragraph", RichTextBlock()),
    ], blank=True, null=True, use_json_field=True)

    gallery = StreamField([
        ("image_list", ListBlock(ImageChooserBlock()))
    ], blank=True, null=True, use_json_field=True)

    testimonials = StreamField([
        ("testimonial", StructBlock([
            ("author", CharBlock()),
            ("quote", RichTextBlock()),
        ])),
    ], blank=True, null=True, use_json_field=True)

    call_to_action = StreamField([
        ("cta", StructBlock([
            ("cta_text", CharBlock()),
            ("cta_link", URLBlock()),
        ])),
    ], blank=True, null=True, use_json_field=True)

    related_articles = StreamField([
        ("related", StructBlock([
            ("title", CharBlock()),
            ("link", URLBlock()),
            ("image", ImageChooserBlock(required=False)),
        ])),
    ], blank=True, null=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel("feature_image"),
        FieldPanel("excerpt"),
        FieldPanel("author"),
        FieldPanel("publication_date"),
        FieldPanel("views_count"),
        FieldPanel("category"),
        FieldPanel("tags"),
        FieldPanel("body"),
        FieldPanel("additional_info"),
        FieldPanel("gallery"),
        FieldPanel("testimonials"),
        FieldPanel("call_to_action"),
        FieldPanel("related_articles"),
    ]

    class Meta:
        verbose_name = "NightFuryPage"
        verbose_name_plural = "NightFuryPages"
        default_related_name = "custom_NightFury_pages"


@register_setting
class NightFuryNavSettings(BaseGenericSetting):
    address = RichTextField(blank=True)

    contact_email = models.TextField(verbose_name="Email", blank=True)
    contact_phone = models.TextField(
        verbose_name="Phone Number",
        blank=True,
        max_length=25,
        help_text="Enter phone number in the format: '+999999999'.",
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'."
            )
        ]
    )

    instagram_url = models.URLField(verbose_name="Instagram Home Page", blank=True)
    facebook_url = models.URLField(verbose_name="Facebook Home Page", blank=True)
    youtube_url = models.URLField(verbose_name="YouTube Home Page", blank=True)
    twitter_url = models.URLField(verbose_name="Twitter Home Page", blank=True)

    current_year = datetime.now().year

    panels = [
        MultiFieldPanel([FieldPanel("address")], heading="Address Information"),
        MultiFieldPanel([FieldPanel("contact_email"), FieldPanel("contact_phone")], heading="Contact Information"),
        MultiFieldPanel([
            FieldPanel("instagram_url"),
            FieldPanel("facebook_url"),
            FieldPanel("youtube_url"),
            FieldPanel("twitter_url"),
        ], heading="Social Media")
    ]

    edit_handler = MultiFieldPanel(panels, heading="Navigation Settings")

    class Meta:
        verbose_name = "Navigation Settings"
        app_label = "base"
