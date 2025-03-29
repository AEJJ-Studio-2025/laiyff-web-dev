from django.db import models

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, InlinePanel
from modelcluster.fields import ParentalKey
from .blocks import FilmDisplayBlock


class HomePageAccordion(Orderable):
    """Model for storing title-content pairs in an accordion format."""
    id = models.BigAutoField(primary_key=True)
    page = ParentalKey("HomePage", related_name="accordion_items", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, help_text="Accordion Title")
    content = RichTextField(blank=True, help_text="Accordion Content")

    panels = [
        FieldPanel("title"),
        FieldPanel("content"),
    ]

    def __str__(self):
        return self.title


class HomePage(Page):
    """Model for the Home Page with an accordion section."""
    heroSectionVideo = models.FileField(upload_to="videos/", blank=True, null=True)
    heroText = models.CharField(help_text="Title of the Page", default="Welcome to Los Angeles International Film Festival", max_length=200)
    introText = models.TextField(blank=True, help_text="Description of Our Film Festival")
    films = StreamField([
        ('film', FilmDisplayBlock()),
    ], blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('heroSectionVideo'),
        FieldPanel('heroText'),
        FieldPanel('introText'),
        FieldPanel('films'),
    ]
