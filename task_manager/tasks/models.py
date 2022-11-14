from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ..statuses.models import Status
from ..labels.models import Label

USER_MODEL = get_user_model()


class Task(models.Model):
    name = models.CharField(_("Name"), unique=True, max_length=100)
    author = models.ForeignKey(
        USER_MODEL,
        verbose_name=_("Author"),
        related_name="tasks",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    description = models.TextField(_("Description"), blank=True)
    status = models.ForeignKey(
        Status, verbose_name=_("Status"), on_delete=models.PROTECT
    )
    executor = models.ForeignKey(
        USER_MODEL,
        verbose_name=_("Executor"),
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    labels = models.ManyToManyField(Label, verbose_name=_("Labels"), through="TaskLabels")
    creation_date = models.DateTimeField(
        _("Creation date"), default=timezone.now
    )

    def __str__(self):
        return f"{self.name}"


class TaskLabels(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    labels = models.ForeignKey(Label, on_delete=models.PROTECT)
