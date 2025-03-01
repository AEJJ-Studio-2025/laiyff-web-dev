from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

class AccordionItemBlock(blocks.StructBlock):
    """A single item inside the accordion"""
    title = blocks.CharBlock(required=True, help_text="Accordion Item Title")
    content = blocks.RichTextBlock(required=True, help_text="Accordion Content")

    class Meta:
        template = "sub_components/accordion_item.html"
        icon = "list-ul"
        label = "Accordion Item"

class AccordionBlock(blocks.StructBlock):
    """Accordion Block that allows multiple collapsible items"""
    items = blocks.ListBlock(AccordionItemBlock(), help_text="Add multiple accordion items")

    class Meta:
        template = "sub_components/accordion_block.html"
        icon = "list-ul"
        label = "Accordion"


class CardBlock(blocks.StructBlock):
    """Card component for images, text, and actions"""
    image = ImageChooserBlock(required=False, help_text="Optional card image")
    title = blocks.CharBlock(required=True, help_text="Card Title")
    description = blocks.TextBlock(required=True, help_text="Card Description")

    class Meta:
        template = "sub_components/card_block.html"
        icon = "image"
        label = "Card"

class TabBlock(blocks.StructBlock):
    """Tab section for switching between content"""
    tab_title = blocks.CharBlock(required=True, help_text="Tab Title")
    tab_content = blocks.RichTextBlock(required=True, help_text="Tab Content")

    class Meta:
        template = "sub_components/tab_block.html"
        icon = "table"
        label = "Tab"

class TimelineItemBlock(blocks.StructBlock):
    """A single event in a Timeline"""
    event_date = blocks.DateBlock(required=True, help_text="Event Date")
    event_title = blocks.CharBlock(required=True, help_text="Event Title")
    event_description = blocks.TextBlock(required=True, help_text="Event Description")

    class Meta:
        template = "sub_components/timeline_item.html"
        icon = "date"
        label = "Timeline Item"

class TimelineBlock(blocks.StructBlock):
    """Timeline section to display events in chronological order"""
    timeline_items = blocks.ListBlock(TimelineItemBlock(), help_text="Add timeline events")

    class Meta:
        template = "sub_components/timeline_block.html"
        icon = "date"
        label = "Timeline"
