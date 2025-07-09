import django_filters
from django.db.models import Count, Q
from django_filters import rest_framework as filters

from api.common.enums import EmploymentType, WorkFormat, WorkSchedule, PaymentFrequency, Currency, WorkExperience
from api.common.filters import MultipleChoiceFilter
from api.vacancies.models import Vacancy


class VacancyFilter(django_filters.FilterSet):
    salary_from = django_filters.NumberFilter(field_name="salary_from", lookup_expr="gte")
    salary_to = django_filters.NumberFilter(field_name="salary_to", lookup_expr="lte")
    is_salary_gross = django_filters.BooleanFilter(field_name="is_salary_gross")
    currency = django_filters.ChoiceFilter(choices=Currency.choices, field_name="currency")
    organization = django_filters.NumberFilter(field_name="organization")
    city = django_filters.NumberFilter(field_name="city")
    specializations = django_filters.BaseInFilter(field_name="specializations__id", lookup_expr="in")

    work_experience = MultipleChoiceFilter(choices=WorkExperience.choices)
    employment_type = MultipleChoiceFilter(choices=EmploymentType.choices)
    work_format = MultipleChoiceFilter(choices=WorkFormat.choices)
    work_schedule = MultipleChoiceFilter(choices=WorkSchedule.choices)
    payment_frequency = MultipleChoiceFilter(choices=PaymentFrequency.choices)

    is_active = django_filters.BooleanFilter(field_name="is_active")

    resume_id = filters.NumberFilter(method="filter_by_resume_skills")

    class Meta:
        model = Vacancy
        fields = []

    def filter_by_resume_skills(self, queryset, name, value):
        from api.resumes.models import Resume

        try:
            resume = Resume.objects.prefetch_related("skills").get(pk=value)
        except Resume.DoesNotExist:
            return queryset.none()

        resume_skill_ids = resume.skills.values_list("id", flat=True)

        queryset = queryset.annotate(
            matching_skills=Count("skills", filter=Q(skills__in=resume_skill_ids))
        ).filter(matching_skills__gte=3)

        return queryset
