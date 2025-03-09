from wagtail import blocks
from .sub_blocks import *


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
