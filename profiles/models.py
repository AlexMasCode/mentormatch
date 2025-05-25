from django.contrib.auth.hashers import make_password
from django_prometheus.models import ExportModelOperationsMixin
from django.db import models

class CatalogIndustry(
    ExportModelOperationsMixin('catalog_industry'),
    models.Model
):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class CatalogField(
    ExportModelOperationsMixin('catalog_field'),
    models.Model
):
    industry = models.ForeignKey(
        CatalogIndustry,
        on_delete=models.CASCADE,
        related_name='fields'
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Skill(
    ExportModelOperationsMixin('skill'),
    models.Model
):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Company(
    ExportModelOperationsMixin('company'),
    models.Model
):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    industry = models.ForeignKey(
        CatalogIndustry,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="companies"
    )
    access_key_hash = models.CharField(max_length=128, blank=True, null=True)
    logo_url = models.URLField(max_length=255, blank=True, null=True)
    specializations = models.ManyToManyField(
        CatalogField,
        blank=True,
        related_name="companies"
    )

    def __str__(self):
        return self.name

    def set_access_key(self, raw_key):
        self.access_key_hash = make_password(raw_key)


class MentorProfile(
    ExportModelOperationsMixin('mentor_profile'),
    models.Model
):
    user_id = models.IntegerField(unique=True)
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    bio = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    skills = models.ManyToManyField(
        Skill,
        through='MentorSkill',
        related_name='mentors'
    )
    specializations = models.ManyToManyField(
        CatalogField,
        through='MentorSpecialization',
        related_name='mentor_specializations'
    )

    def __str__(self):
        return f"MentorProfile (user_id={self.user_id})"


class MentorSkill(
    ExportModelOperationsMixin('mentor_skill'),
    models.Model
):
    mentor = models.ForeignKey(
        MentorProfile,
        on_delete=models.CASCADE,
        db_index=True
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        db_index=True
    )

    class Meta:
        unique_together = ('mentor', 'skill')
        indexes = [
            models.Index(fields=['mentor']),
            models.Index(fields=['skill']),
        ]


class MentorSpecialization(
    ExportModelOperationsMixin('mentor_specialization'),
    models.Model
):
    mentor = models.ForeignKey(
        MentorProfile,
        on_delete=models.CASCADE,
        db_index=True
    )
    field = models.ForeignKey(
        CatalogField,
        on_delete=models.CASCADE,
        db_index=True
    )

    class Meta:
        unique_together = ('mentor', 'field')
        indexes = [
            models.Index(fields=['mentor']),
            models.Index(fields=['field']),
        ]


class MenteeProfile(
    ExportModelOperationsMixin('mentee_profile'),
    models.Model
):
    user_id = models.IntegerField(unique=True)
    development_goals = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    skills = models.ManyToManyField(
        Skill,
        through='MenteeSkill',
        related_name='mentees'
    )
    desired_fields = models.ManyToManyField(
        CatalogField,
        through='MenteeDesiredField',
        related_name='desired_by_mentees'
    )

    def __str__(self):
        return f"MenteeProfile (user_id={self.user_id})"


class MenteeSkill(
    ExportModelOperationsMixin('mentee_skill'),
    models.Model
):
    mentee = models.ForeignKey(
        MenteeProfile,
        on_delete=models.CASCADE,
        db_index=True
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        db_index=True
    )

    class Meta:
        unique_together = ('mentee', 'skill')
        indexes = [
            models.Index(fields=['mentee']),
            models.Index(fields=['skill']),
        ]


class MenteeDesiredField(
    ExportModelOperationsMixin('mentee_desired_field'),
    models.Model
):
    mentee = models.ForeignKey(
        MenteeProfile,
        on_delete=models.CASCADE,
        db_index=True
    )
    field = models.ForeignKey(
        CatalogField,
        on_delete=models.CASCADE,
        db_index=True
    )

    class Meta:
        unique_together = ('mentee', 'field')
        indexes = [
            models.Index(fields=['mentee']),
            models.Index(fields=['field']),
        ]
