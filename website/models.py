from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from .blocks import ContentBlock
from modelcluster.fields import ParentalKey
from wagtail.images.models import Image



class CarouselImages(models.Model):
    Page = ParentalKey("NormalPage", on_delete=models.CASCADE, related_name="carousel_images")
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="+")

    panels = [
        FieldPanel("image"),
    ]  

class NormalPage(Page):
    """A page model that allows only 0 or 1 Hero Section but unlimited other components"""

    heroTitle = models.TextField(blank=True, help_text="Description of Our Film Festival")
    body = RichTextField(blank=True)

    HERO_CHOICES = [
        ('Image', 'Use background image'),
        ('Video', 'Use background video'),
        ('Carousel', 'Carousel'),
    ]

    heroType = models.CharField(
        max_length=20,
        choices=HERO_CHOICES,
        default='option1',
    )

    heroSectionVideo = models.FileField(upload_to="videos/", blank=True, null=True)
    heroSectionImage = models.FileField(upload_to="images/", blank=True, null=True)

    components = StreamField([
        ('content_block', ContentBlock()),  
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("heroTitle"),
        FieldPanel("body"),
        FieldPanel("heroType"),
        FieldPanel("heroSectionVideo"),
        FieldPanel("heroSectionImage"),
        InlinePanel("carousel_images", label="Carousel Images"),
        FieldPanel("components"),
    ]

    class Meta:
        verbose_name = "Normal Page"
