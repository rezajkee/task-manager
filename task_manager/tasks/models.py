from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ..statuses.models import Status
from ..tags.models import Tag

USER_MODEL = get_user_model()


def get_full_name(self):
    return f"{self.first_name} {self.last_name}"


# Inject get_full_name method instead of __str__ to User model
USER_MODEL.add_to_class("__str__", get_full_name)


# class FullNamedUser(USER_MODEL):
#     """Proxy model for a User model.
#     Adds fullname __str__ method."""
#     class Meta:
#         proxy = True

#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"


class Task(models.Model):
    name = models.CharField(_("NameTitle"), max_length=100)
    author = models.ForeignKey(
        USER_MODEL,
        verbose_name=_("AuthorTitle"),
        related_name="tasks",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    description = models.TextField(_("DescriptionTitle"), blank=True)
    status = models.ForeignKey(
        Status, verbose_name=_("StatusTitle"), on_delete=models.PROTECT
    )
    doer = models.ForeignKey(
        USER_MODEL,
        verbose_name=_("DoerTitle"),
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    tags = models.ManyToManyField(Tag, verbose_name=_("TagsTitle"), blank=True)
    creation_date = models.DateTimeField(
        _("CreationDateTitle"), default=timezone.now
    )

    def __str__(self):
        return f"{self.name}"
