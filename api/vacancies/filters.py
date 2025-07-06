import django_filters
from api.vacancies.models import Vacancy


class VacancyFilter(django_filters.FilterSet):
    salary_from = django_filters.NumberFilter(field_name="salary_from", lookup_expr="gte")
    salary_to = django_filters.NumberFilter(field_name="salary_to", lookup_expr="lte")
    organization = django_filters.NumberFilter(field_name="organization")
    city = django_filters.NumberFilter(field_name="city")
    work_experience = django_filters.CharFilter(field_name="work_experience")
    is_salary_gross = django_filters.BooleanFilter(field_name="is_salary_gross")
    specializations = django_filters.BaseInFilter(field_name="specializations__id", lookup_expr="in")

    class Meta:
        model = Vacancy
        fields = []
