from django.contrib import admin

from .models import Status


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "creation_date",
    )
    list_editable = ("name",)
