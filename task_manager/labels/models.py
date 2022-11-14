from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    name = models.CharField(_("Name"), unique=True, max_length=100)
    creation_date = models.DateTimeField(
        _("Creation date"), default=timezone.now
    )

    def __str__(self):
        return f"{self.name}"