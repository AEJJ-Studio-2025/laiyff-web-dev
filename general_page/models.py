from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.images.models import Image
from wagtail.blocks import CharBlock, RichTextBlock, StructBlock, URLBlock, ListBlock
from wagtail.images.blocks import ImageChooserBlock
from django.db import models

class GeneralPage(Page):
    template = "general_page.html"
    
    feature_image = models.ForeignKey(
        Image, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name='+'  # Prevents reverse relation
    )
    
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
    
    content_panels = Page.content_panels + [
        FieldPanel("feature_image"),
        FieldPanel("body", classname="full"),
        FieldPanel("additional_info"),
        FieldPanel("gallery"),
        FieldPanel("testimonials"),
        FieldPanel("call_to_action"),
    ]
    
    class Meta:
        verbose_name = "General Page"
        verbose_name_plural = "General Pages"
