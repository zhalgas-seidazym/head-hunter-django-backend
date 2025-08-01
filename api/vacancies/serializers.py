from rest_framework import serializers
from api.vacancies.models import Vacancy
from api.skills.models import Skill
from api.specializations.models import Specialization
from api.organizations.models import Organization
from api.locations.models import City
from api.common.enums import WorkExperience, PaymentFrequency, EmploymentType, WorkFormat, WorkSchedule, Currency


class VacancySerializer(serializers.ModelSerializer):
    skills = serializers.PrimaryKeyRelatedField(many=True, queryset=Skill.objects.all(), required=False)
    specializations = serializers.PrimaryKeyRelatedField(many=True, queryset=Specialization.objects.all(), required=False)
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), allow_null=True, required=False)

    work_experience = serializers.ChoiceField(choices=WorkExperience.choices, default=WorkExperience.NO_EXPERIENCE)
    payment_frequency = serializers.ChoiceField(choices=PaymentFrequency.choices, default=PaymentFrequency.MONTHLY)
    employment_type = serializers.ChoiceField(choices=EmploymentType.choices, default=EmploymentType.FULL_TIME)
    work_format = serializers.ChoiceField(choices=WorkFormat.choices, default=WorkFormat.ON_SITE)
    work_schedule = serializers.ChoiceField(choices=WorkSchedule.choices, default=WorkSchedule.FULL_DAY)
    currency = serializers.ChoiceField(choices=Currency.choices, default=Currency.KZT)

    class Meta:
        model = Vacancy
        fields = [
            "id",
            "title",
            "description",
            "salary_from",
            "salary_to",
            "is_salary_gross",
            "payment_frequency",
            "currency",
            "organization",
            "created_by",
            "city",
            "specializations",
            "skills",
            "work_experience",
            "employment_type",
            "work_format",
            "work_schedule",
            "is_active",
            "created_at",
            "updated_at"
        ]
        read_only_fields = ("id", "created_by", "created_at", "updated_at")
