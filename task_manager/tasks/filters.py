import django_filters
from .models import Task
from ..labels.models import Label
from django.utils.translation import gettext_lazy as _
from django.forms import CheckboxInput


class TaskFilter(django_filters.FilterSet):
    label = django_filters.ModelChoiceFilter(field_name='labels', label=_("Label"), lookup_expr='exact', queryset=Label.objects.all())
    self_tasks = django_filters.BooleanFilter(label=_("Your own tasks only"), field_name='author', method='filter_user_is_an_author', widget=CheckboxInput)

    class Meta:
        model = Task
        fields = {'status': ['exact'], 'executor': ['exact']}

    def filter_user_is_an_author(self, queryset, name, value):
        if value:
            return queryset.filter(**{name: self.request.user})
        else:
            return queryset
