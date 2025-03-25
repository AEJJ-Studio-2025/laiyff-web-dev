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

from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class HomePage(Page):
    """Model for the Home Page with an accordion section."""
    heroSectionVideo = models.FileField(upload_to="videos/", blank=True, null=True)
    introText = models.TextField(blank=True, help_text="Description of Our Film Festival")
    body = RichTextField(blank=True)
    films = StreamField([
        ('film', FilmDisplayBlock()),
    ], blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('heroSectionVideo'),
        FieldPanel('introText'),
        InlinePanel('accordion_items', label="Accordion Sections"), 
        FieldPanel('body'),
        FieldPanel('films'),
    ]

    def get_accordion_pairs(self):
        """Returns the accordion items as (title, content) pairs."""
        return [(item.title, item.content) for item in self.accordion_items.all()]
