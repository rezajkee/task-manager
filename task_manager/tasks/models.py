from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from ..statuses.models import Status
from django.conf import settings


USER_MODEL = get_user_model()


class Task(models.Model):
    name = models.CharField(_("NameTitle"), max_length=100)
    author = models.ForeignKey(USER_MODEL, verbose_name=_("AuthorTitle"), related_name="tasks", null=True, blank=True, on_delete=models.CASCADE)
    description = models.TextField(_("DescriptionTitle"), blank=True)
    status = models.ForeignKey(Status, verbose_name=_("StatusTitle"), on_delete=models.PROTECT)
    doer = models.ForeignKey(USER_MODEL, verbose_name=_("DoerTitle"), blank=True, null=True, on_delete=models.SET_NULL)
    creation_date = models.DateTimeField(
        _("CreationDateTitle"), default=timezone.now
    )

    def __str__(self):
        return f"{self.name}"

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)