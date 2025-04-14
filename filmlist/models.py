from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import CharBlock, StructBlock, ListBlock, DateBlock
from datetime import date, timedelta, datetime


class MovieBlock(StructBlock):
    start_date = DateBlock(label="Start Date")
    end_date = DateBlock(label="End Date")
    category = CharBlock(label="Category")
    title = CharBlock(label="Title")
    director = CharBlock(label="Director")
    times = ListBlock(CharBlock(label="Showtime"))
    image = ImageChooserBlock(required=False)
    link = CharBlock(label="Link (optional)", required=False)

    class Meta:
        icon = "film"
        label = "Movie"
        form_classname = "movie-block"


class MovieListPage(Page):
    template = "movielist.html"

    date_label = models.CharField(max_length=50, default="Today")
    date_value = models.DateField(default=date.today)
    available_dates = models.JSONField(default=list, blank=True)

    movies = StreamField([
        ("movie", MovieBlock())
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("date_label"),
        FieldPanel("date_value"),
        FieldPanel("available_dates"),
        FieldPanel("movies"),
    ]

    def save(self, *args, **kwargs):
        if not self.available_dates:
            today = date.today()
            self.available_dates = [(today + timedelta(days=i)).isoformat() for i in range(14)]
        super().save(*args, **kwargs)

    def get_context(self, request):
        context = super().get_context(request)

        date_str = request.GET.get("date")
        category_filter = request.GET.get("category", "").strip().lower()
        selected_date = self.date_value

        if date_str:
            try:
                selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                self.date_label = "Selected"
            except ValueError:
                pass

        movies_for_date = []
        categories_set = set()

        for block in self.movies:
            if block.block_type != "movie":
                continue

            value = block.value
            start = value.get("start_date")
            end = value.get("end_date")
            category = value.get("category", "").strip()

            if start and end and start <= selected_date <= end:
                categories_set.add(category)
                if not category_filter or category.lower() == category_filter:
                    movies_for_date.append(block)

        parsed_dates = []
        for d in self.available_dates:
            try:
                parsed = datetime.strptime(d, "%Y-%m-%d").date()
                parsed_dates.append(parsed)
            except Exception:
                pass

        context.update({
            "page": self,
            "available_dates_parsed": parsed_dates,
            "selected_date": selected_date,
            "movies_for_date": movies_for_date,
            "date_label": self.date_label,
            "active_category": category_filter,
            "available_categories": sorted(categories_set),
            "today": date.today()
        })

        return context
