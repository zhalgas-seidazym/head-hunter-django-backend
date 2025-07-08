import django_filters


class MultipleChoiceFilter(django_filters.BaseInFilter, django_filters.ChoiceFilter):
    pass