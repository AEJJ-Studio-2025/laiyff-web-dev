from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class FilmDisplayBlock(blocks.StructBlock):
    """Block for film display"""
    title = blocks.CharBlock(required=True, help_text="Film Title")
    image = ImageChooserBlock(required=False, help_text="Optional card image")
    href = blocks.CharBlock(required=True, help_text="Redirect to: ")

    class Meta:
        template = "blocks/film_display_block.html"
        label = "Film Display Block"
        
