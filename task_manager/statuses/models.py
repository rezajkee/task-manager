from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    name = models.CharField(_("NameTitle"), unique=True, max_length=100)
    creation_date = models.DateTimeField(
        _("CreationDateTitle"), default=timezone.now
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Statuses"
