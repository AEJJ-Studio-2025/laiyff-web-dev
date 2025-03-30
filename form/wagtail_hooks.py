from wagtail import hooks
from django.urls import reverse
from wagtail.admin.menu import MenuItem


@hooks.register("register_admin_menu_item")
def register_form_submission_menu_item():
    return MenuItem(
        "Form Submissions",
        reverse("admin:form_formpagesubmission_changelist"),  # Django Admin URL
        icon_name="form",
        order=600
    )
