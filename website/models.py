from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from .blocks import HeroSectionBlock, ContentBlock

class NormalPage(Page):
    """A page model that allows only 0 or 1 Hero Section but unlimited other components"""

    components = StreamField([
        ('hero_section', HeroSectionBlock()),  
        ('content_block', ContentBlock()),  
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("components"),
    ]

    class Meta:
        verbose_name = "Normal Page"
