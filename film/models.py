from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class FilmPage(Page):
    name = models.CharField(blank=True, help_text="Film Title", max_length=512)
    description = RichTextField(blank=True, help_text="Film Description")
    photo = models.FileField(upload_to="images/", blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel("name"), 
        FieldPanel("description"),
        FieldPanel("photo"),
    ]
