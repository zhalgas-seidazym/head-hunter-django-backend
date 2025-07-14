from django_filters import FilterSet, NumberFilter, CharFilter, ChoiceFilter, ModelChoiceFilter
from django_filters.filters import BaseInFilter
from datetime import datetime
from django.db.models import Count, Q

from api.locations.models import City
from api.common.enums import WorkExperience, EducationDegree
from api.resumes.models import Resume
from api.vacancies.models import Vacancy


class JSONInOverlapFilter(BaseInFilter):
    def filter(self, qs, value):
        if value:
            return qs.filter(**{f"{self.field_name}__overlap": list(value)})
        return qs


class ResumeFilter(FilterSet):
    user = NumberFilter(field_name="user", lookup_expr="exact")
    expected_salary_from = NumberFilter(field_name="expected_salary", lookup_expr="gte")
    expected_salary_to = NumberFilter(field_name="expected_salary", lookup_expr="lte")
    currency = CharFilter(field_name="currency")

    specializations = BaseInFilter(field_name="specializations__id", lookup_expr="in")

    employment_type = JSONInOverlapFilter(field_name="employment_types")
    work_schedule = JSONInOverlapFilter(field_name="work_schedules")
    work_format = JSONInOverlapFilter(field_name="work_formats")
    payment_frequency = JSONInOverlapFilter(field_name="payment_frequencies")

    city = ModelChoiceFilter(field_name="user__city", queryset=City.objects.all())

    degree = ChoiceFilter(method="filter_by_degree", choices=EducationDegree.choices)
    experience_level = ChoiceFilter(method="filter_by_experience_level", choices=WorkExperience.choices)

    vacancy_id = NumberFilter(method="filter_by_vacancy_skills")

    class Meta:
        model = Resume
        fields = []

    def filter_by_degree(self, queryset, name, value):
        return queryset.filter(educations__degree=value).distinct()

    def filter_by_experience_level(self, queryset, name, value):
        now = datetime.now()
        resume_ids = []

        for resume in queryset.prefetch_related("experiences"):
            total_months = 0
            for exp in resume.experiences.all():
                try:
                    start = datetime(exp.start_year, exp.start_month, 1)
                    end = now if exp.currently_working else datetime(exp.end_year, exp.end_month, 1)
                    months = (end.year - start.year) * 12 + (end.month - start.month)
                    total_months += max(months, 0)
                except:
                    continue

            if (
                (value == WorkExperience.NO_EXPERIENCE and total_months == 0) or
                (value == WorkExperience.LESS_THAN_ONE and 0 < total_months < 12) or
                (value == WorkExperience.ONE_TO_THREE and 12 <= total_months < 36) or
                (value == WorkExperience.THREE_TO_FIVE and 36 <= total_months < 60) or
                (value == WorkExperience.MORE_THAN_FIVE and total_months >= 60)
            ):
                resume_ids.append(resume.id)

        return queryset.filter(id__in=resume_ids)

    def filter_by_vacancy_skills(self, queryset, name, value):
        try:
            vacancy = Vacancy.objects.prefetch_related("skills").get(id=value)
        except Vacancy.DoesNotExist:
            return queryset.none()

        vacancy_skill_ids = vacancy.skills.values_list("id", flat=True)

        queryset = queryset.annotate(
            matching_skills=Count("skills", filter=Q(skills__in=vacancy_skill_ids))
        ).filter(matching_skills__gte=3)

        return queryset
