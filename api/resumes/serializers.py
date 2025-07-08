from rest_framework import serializers

from api.resumes.models import (
    Resume, ResumeExperience, ResumeEducation, ResumeCourse
)
from api.common.enums import (
    EmploymentType, WorkSchedule, WorkFormat, PaymentFrequency
)
from api.skills.models import Skill
from api.specializations.models import Specialization
from api.organizations.models import Industry
from api.locations.models import City


class EnumListField(serializers.ListField):
    """
    Список строк, каждая должна входить в enum (choices).
    """
    def __init__(self, *, enum_class, **kwargs):
        super().__init__(
            child=serializers.ChoiceField(choices=enum_class.choices),
            **kwargs
        )



class ResumeExperienceSerializer(serializers.ModelSerializer):
    resume = serializers.PrimaryKeyRelatedField(queryset=Resume.objects.all())
    city = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(), allow_null=True, required=False
    )
    industries = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Industry.objects.all(), required=False
    )
    specializations = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Specialization.objects.all(), required=False
    )

    class Meta:
        model = ResumeExperience
        fields = [
            "id",
            "resume",
            "company_name",
            "city",
            "company_website",
            "industries",
            "specializations",
            "start_month",
            "start_year",
            "currently_working",
            "end_month",
            "end_year",
            "responsibilities",
        ]



class ResumeEducationSerializer(serializers.ModelSerializer):
    resume = serializers.PrimaryKeyRelatedField(queryset=Resume.objects.all())

    class Meta:
        model = ResumeEducation
        fields = [
            "id",
            "resume",
            "degree",
            "institution_name",
            "faculty",
            "specialization",
            "graduation_year",
        ]



class ResumeCourseSerializer(serializers.ModelSerializer):
    resume = serializers.PrimaryKeyRelatedField(queryset=Resume.objects.all())

    class Meta:
        model = ResumeCourse
        fields = [
            "id",
            "resume",
            "course_name",
            "organization",
            "specialization",
            "graduation_year",
        ]



class ResumeSerializer(serializers.ModelSerializer):
    skills = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Skill.objects.all(), required=False
    )
    specializations = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Specialization.objects.all()
    )

    # enum-списки с валидацией
    employment_types = EnumListField(enum_class=EmploymentType, required=False)
    work_schedules = EnumListField(enum_class=WorkSchedule, required=False)
    work_formats = EnumListField(enum_class=WorkFormat, required=False)
    payment_frequencies = EnumListField(enum_class=PaymentFrequency, required=False)

    # вложенные коллекции (только чтение)
    educations = ResumeEducationSerializer(many=True, read_only=True)
    experiences = ResumeExperienceSerializer(many=True, read_only=True)
    courses = ResumeCourseSerializer(many=True, read_only=True)

    class Meta:
        model = Resume
        fields = [
            "id",
            "user",
            "title",
            "about",
            "expected_salary",
            "currency",
            "phone",
            "email",
            "employment_types",
            "work_schedules",
            "work_formats",
            "payment_frequencies",
            "skills",
            "specializations",
            "educations",
            "experiences",
            "courses",
        ]
        read_only_fields = ("id", "user")
