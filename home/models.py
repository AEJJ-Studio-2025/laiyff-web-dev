from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel, InlinePanel
from modelcluster.fields import ParentalKey
from .blocks import FilmDisplayBlock
from wagtail.images.models import Image


class CarouselImages(models.Model):
    Page = ParentalKey("HomePage", on_delete=models.CASCADE, related_name="carousel_images")
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="+")
    id = models.BigAutoField(primary_key=True)

    panels = [
        FieldPanel("image"),
    ]  


class HomePage(Page):
    """Model for the Home Page with an accordion section."""
    heroText = models.CharField(help_text="Title of the Page", default="Welcome to Los Angeles International Film Festival", max_length=200)
    introText = models.TextField(blank=True, help_text="Description of Our Film Festival")
    films = StreamField([
        ('film', FilmDisplayBlock()),
    ], blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        InlinePanel("carousel_images", label="Carousel Images"),
        FieldPanel('heroText'),
        FieldPanel('introText'),
        FieldPanel('films'),
    ]
