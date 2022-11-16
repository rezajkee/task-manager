import django_filters
from .models import Task
from ..labels.models import Label
from django.utils.translation import gettext_lazy as _
from django.forms import CheckboxInput


def get_all_labels(request):
    return Label.objects.all()


def user_is_author(request):
    return Task.objects.filter(author=request.user)


class TaskFilter(django_filters.FilterSet):
    # status = django_filters.CharFilter(field_name=_("Status"), lookup_expr='exact')
    # executor = django_filters.CharFilter(field_name=_("Executor"), lookup_expr='exact')
    label = django_filters.ModelChoiceFilter(field_name='labels', label=_("Label"), lookup_expr='exact', queryset=get_all_labels)
    self_tasks = django_filters.ModelChoiceFilter(queryset=user_is_author, widget=CheckboxInput)

    class Meta:
        model = Task
        fields = {'status': ['exact'], 'executor': ['exact']}


# def departments(request):
#     company = request.user.company
#     return company.department_set.all()

# class EmployeeFilter(filters.FilterSet):
#     department = filters.ModelChoiceFilter(queryset=departments)
#     ...
# The above example restricts the set of departments to those in the logged-in user's associated company.

# author = Task.objects.get(id=self.kwargs["pk"]).author
#         return self.request.user == author