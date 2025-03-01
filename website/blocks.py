from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from .sub_blocks import *

class HeroSectionBlock(blocks.StructBlock):
    """Hero Section with options for Banner, Carousel, or Jumbotron"""
    
    hero_type = blocks.ChoiceBlock(
        choices=[
            ('hero', 'Hero Section'),
            ('carousel', 'Carousel'),
            ('jumbotron', 'Jumbotron'),
        ],
        default='hero',
        help_text="Select the type of hero section"
    )

    title = blocks.CharBlock(required=True, help_text="Main headline")
    subtitle = blocks.TextBlock(required=False, help_text="Subtext below the title")
    background_image = ImageChooserBlock(required=False, help_text="Background image")
    background_video = DocumentChooserBlock(required=False, help_text="Upload a background video")

    carousel_images = blocks.ListBlock(
        ImageChooserBlock(), help_text="Add multiple images for the carousel", required=False
    )

    class Meta:
        template = "components/hero_section.html"
        icon = "image"
        label = "Hero Section"



class ContentBlock(blocks.StructBlock):
    """Text Content with Title and Content Display Components"""
    title = blocks.CharBlock(required=True, help_text="Section Title")
    content_display_components = blocks.ListBlock(
        blocks.StreamBlock([
            ('accordion', AccordionBlock()),
            ('card', CardBlock()),
            ('tab', TabBlock()),
            ('timeline', TimelineBlock()),
        ], required=False),
        help_text="Add content display components"
    )

    class Meta:
        template = "components/content_block.html"
        icon = "doc-full"
        label = "Content Display"



# Custom StreamBlock to enforce constraints
class NormalPageStreamBlock(blocks.StreamBlock):
    """A StreamBlock that allows only 0 or 1 HeroSectionBlock and multiple other blocks"""
    hero_section = blocks.ListBlock(HeroSectionBlock(), max_num=1, required=False)
    content_block = blocks.ListBlock(ContentBlock(), required=False)
