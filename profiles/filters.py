import django_filters
from .models import MentorProfile, Company, MenteeProfile


class MentorProfileFilter(django_filters.FilterSet):
    # Filter by company ID (exact match)
    company = django_filters.NumberFilter(field_name="company__id", lookup_expr='exact')
    user_id = django_filters.NumberFilter(field_name="user_id", lookup_expr='exact')

    # Filter by company name (case-insensitive partial match)
    company_name = django_filters.CharFilter(field_name="company__name", lookup_expr='icontains')

    # Filter by skills – expects a comma-separated string of skill IDs
    skills = django_filters.CharFilter(method='filter_skills', label="Skills (IDs comma-separated)")

    # Filter by experience – minimum and maximum
    experience_min = django_filters.NumberFilter(field_name='experience_years', lookup_expr='gte')
    experience_max = django_filters.NumberFilter(field_name='experience_years', lookup_expr='lte')

    # Filter by rating – minimum and maximum
    rating_min = django_filters.NumberFilter(field_name='average_rating', lookup_expr='gte')
    rating_max = django_filters.NumberFilter(field_name='average_rating', lookup_expr='lte')

    # Filter by specializations – expects a comma-separated string of CatalogField IDs
    specializations = django_filters.CharFilter(method='filter_specializations',
                                                label="Specializations (IDs comma-separated)")

    class Meta:
        model = MentorProfile
        fields = ['user_id']

    def filter_skills(self, queryset, name, value):
        try:
            skill_ids = [int(x.strip()) for x in value.split(',') if x.strip().isdigit()]
        except ValueError:
            return queryset
        if skill_ids:
            queryset = queryset.filter(skills__id__in=skill_ids).distinct()
        return queryset

    def filter_specializations(self, queryset, name, value):
        try:
            field_ids = [int(x.strip()) for x in value.split(',') if x.strip().isdigit()]
        except ValueError:
            return queryset
        if field_ids:
            queryset = queryset.filter(specializations__id__in=field_ids).distinct()
        return queryset


class CompanyFilter(django_filters.FilterSet):
    # Filter by company name using partial case-insensitive match
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    # Filter by industry via FK – by ID or name
    industry = django_filters.NumberFilter(field_name='industry__id', lookup_expr='exact')
    industry_name = django_filters.CharFilter(field_name='industry__name', lookup_expr='icontains')

    # Filter by specializations – expects a comma-separated string of CatalogField IDs
    specializations = django_filters.CharFilter(method='filter_specializations',
                                                label="Specializations (IDs comma-separated)")

    class Meta:
        model = Company
        fields = []

    def filter_specializations(self, queryset, name, value):
        try:
            spec_ids = [int(x.strip()) for x in value.split(',') if x.strip().isdigit()]
        except ValueError:
            return queryset
        if spec_ids:
            queryset = queryset.filter(specializations__id__in=spec_ids).distinct()
        return queryset


class MenteeProfileFilter(django_filters.FilterSet):
    skills = django_filters.CharFilter(
        method='filter_skills',
        label='Skills (IDs comma-separated)'
    )
    desired_fields = django_filters.CharFilter(
        method='filter_desired_fields',
        label='Desired Fields (IDs comma-separated)'
    )
    # Text search in development_goals
    development_goals = django_filters.CharFilter(
        field_name='development_goals', lookup_expr='icontains'
    )

    class Meta:
        model = MenteeProfile
        fields = []

    def filter_skills(self, queryset, name, value):
        # expect comma-separated skill IDs
        skill_ids = [int(x) for x in value.split(',') if x.strip().isdigit()]
        if skill_ids:
            queryset = queryset.filter(skills__id__in=skill_ids).distinct()
        return queryset

    def filter_desired_fields(self, queryset, name, value):
        field_ids = [int(x) for x in value.split(',') if x.strip().isdigit()]
        if field_ids:
            queryset = queryset.filter(desired_fields__id__in=field_ids).distinct()
        return queryset