from django.db import models


class Role(models.TextChoices):
    APPLICANT = 'applicant', 'Соискатель'
    EMPLOYER = 'employer', 'Работодатель'


class OrganizationRole(models.TextChoices):
    OWNER = 'owner', 'Owner'
    EMPLOYER = 'employer', 'Employer'
    RECRUITER = 'recruiter', 'Recruiter'
    VIEWER = 'viewer', 'Viewer'

ORGANIZATION_ROLE_RANKS = {
    OrganizationRole.OWNER: 3,
    OrganizationRole.EMPLOYER: 2,
    OrganizationRole.RECRUITER: 1,
    OrganizationRole.VIEWER: 0,
}

class OrganizationRequestStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    ACCEPTED = 'accepted', 'Accepted'
    DECLINED = 'declined', 'Declined'

class WorkExperience(models.TextChoices):
    NO_EXPERIENCE = "no_experience", "Нет опыта"
    LESS_THAN_ONE = "less_than_one", "Меньше года"
    ONE_TO_THREE = "one_to_three", "От 1 года до 3 лет"
    THREE_TO_FIVE = "three_to_five", "От 3 до 5 лет"
    MORE_THAN_FIVE = "more_than_five", "Более 5 лет"

class EmploymentType(models.TextChoices):
    FULL_TIME = "FULL_TIME", "Полная занятость"
    PART_TIME = "PART_TIME", "Частичная занятость"
    PROJECT = "PROJECT", "Проектная занятость"
    ROTATIONAL = "ROTATIONAL", "Вахтовый метод"

class WorkFormat(models.TextChoices):
    ON_SITE = "ON_SITE", "На месте работодателя"
    REMOTE = "REMOTE", "Удалённо"
    HYBRID = "HYBRID", "Гибрид"
    FIELD = "FIELD", "Разъездной"

class WorkSchedule(models.TextChoices):
    FULL_DAY = "FULL_DAY", "Полный день"
    SHIFT = "SHIFT", "Сменный график"
    FLEXIBLE = "FLEXIBLE", "Гибкий график"
    REMOTE = "REMOTE", "Удалённая работа"
    ROTATIONAL = "ROTATIONAL", "Вахтовый метод"

class PaymentFrequency(models.TextChoices):
    HOURLY = "HOURLY", "Почасовая оплата"
    DAILY = "DAILY", "Ежедневно"
    WEEKLY = "WEEKLY", "Еженедельно"
    BIWEEKLY = "BIWEEKLY", "Раз в две недели"
    MONTHLY = "MONTHLY", "Ежемесячно"
    QUARTERLY = "QUARTERLY", "Ежеквартально"
    ANNUALLY = "ANNUALLY", "Ежегодно"
    ONE_TIME = "ONE_TIME", "Единовременная выплата"

class Currency(models.TextChoices):
    KZT = "KZT", "₸ Казахстанский тенге"
    RUB = "RUB", "₽ Российский рубль"
    USD = "USD", "$ Доллар США"
    EUR = "EUR", "€ Евро"
    GBP = "GBP", "£ Британский фунт"
    CNY = "CNY", "¥ Китайский юань"
    TRY = "TRY", "₺ Турецкая лира"
    AED = "AED", "د.إ Дирхам ОАЭ"
    UZS = "UZS", "сум Узбекский сум"

class EducationDegree(models.TextChoices):
    SECONDARY = "SECONDARY", "Среднее"
    SPECIAL_SECONDARY = "SPECIAL_SECONDARY", "Среднее специальное"
    INCOMPLETE_HIGHER = "INCOMPLETE_HIGHER", "Неоконченное высшее"
    HIGHER = "HIGHER", "Высшее"
    BACHELOR = "BACHELOR", "Бакалавр"
    MASTER = "MASTER", "Магистр"
    CANDIDATE_SCIENCE = "CANDIDATE_SCIENCE", "Кандидат наук"
    DOCTOR_SCIENCE = "DOCTOR_SCIENCE", "Доктор наук"