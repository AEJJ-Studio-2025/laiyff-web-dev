from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class FilmPage(Page):
    name = models.CharField(blank=True, help_text="Film Title", max_length=512)
    description = RichTextField(blank=True, help_text="Film Description")
    director = models.CharField(blank=True, help_text="Film Director", max_length=200)
    released_year = models.PositiveIntegerField(help_text="Released Date", default=2025)
    genres = models.CharField(
        blank=True,
        help_text="Comma-separated genres (e.g. Sci-Fi, Thriller)",
        max_length=512,
        default=""
    )

    photo = models.FileField(upload_to="images/", blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel("name"), 
        FieldPanel("description"),
        FieldPanel("director"),
        FieldPanel("released_year"),
        FieldPanel("genres"),
        FieldPanel("photo"),
    ]
