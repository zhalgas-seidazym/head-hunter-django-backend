from django_filters import FilterSet, BaseInFilter, CharFilter, NumberFilter, ModelChoiceFilter, ChoiceFilter

from api.common.enums import WorkExperience, EducationDegree
from api.resumes.models import Resume
from api.locations.models import City
from datetime import datetime


class JSONInOverlapFilter(BaseInFilter):
    def filter(self, qs, value):
        if value:
            return qs.filter(**{f"{self.field_name}__overlap": list(value)})
        return qs


class ResumeFilter(FilterSet):
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
