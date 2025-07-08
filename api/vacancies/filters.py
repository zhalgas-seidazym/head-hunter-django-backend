import django_filters

from api.common.enums import EmploymentType, WorkFormat, WorkSchedule, PaymentFrequency, Currency
from api.common.filters import MultipleChoiceFilter
from api.vacancies.models import Vacancy


class VacancyFilter(django_filters.FilterSet):
    salary_from = django_filters.NumberFilter(field_name="salary_from", lookup_expr="gte")
    salary_to = django_filters.NumberFilter(field_name="salary_to", lookup_expr="lte")
    is_salary_gross = django_filters.BooleanFilter(field_name="is_salary_gross")
    currency = django_filters.ChoiceFilter(choices=Currency.choices, field_name="currency")
    organization = django_filters.NumberFilter(field_name="organization")
    city = django_filters.NumberFilter(field_name="city")
    work_experience = django_filters.CharFilter(field_name="work_experience")
    specializations = django_filters.BaseInFilter(field_name="specializations__id", lookup_expr="in")

    employment_type = MultipleChoiceFilter(choices=EmploymentType.choices)
    work_format = MultipleChoiceFilter(choices=WorkFormat.choices)
    work_schedule = MultipleChoiceFilter(choices=WorkSchedule.choices)
    payment_frequency = MultipleChoiceFilter(choices=PaymentFrequency.choices)

    is_active = django_filters.BooleanFilter(field_name="is_active")

    class Meta:
        model = Vacancy
        fields = []
