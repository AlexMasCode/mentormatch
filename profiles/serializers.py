from rest_framework import serializers
from .models import (
    Company, CatalogIndustry, CatalogField, Skill,
    MentorProfile, MentorSkill, MentorSpecialization,
    MenteeProfile, MenteeSkill, MenteeDesiredField
)


class CatalogIndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogIndustry
        fields = ['id', 'name']


class CatalogFieldSerializer(serializers.ModelSerializer):
    industry = CatalogIndustrySerializer(read_only=True)
    industry_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = CatalogField
        fields = ['id', 'name', 'industry', 'industry_id']


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']


class CompanySerializer(serializers.ModelSerializer):
    industry = CatalogIndustrySerializer(read_only=True)
    industry_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    specializations = CatalogFieldSerializer(many=True, read_only=True)
    specializations_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )

    class Meta:
        model = Company
        fields = [
            'id', 'name', 'description',
            'industry', 'industry_id', 'logo_url',
            'specializations', 'specializations_ids'
        ]

    def create(self, validated_data):
        industry_id = validated_data.pop('industry_id', None)
        specializations_ids = validated_data.pop('specializations_ids', [])
        if industry_id:
            from .models import CatalogIndustry
            validated_data['industry'] = CatalogIndustry.objects.get(id=industry_id)
        company = Company.objects.create(**validated_data)
        if specializations_ids:
            company.specializations.set(specializations_ids)
        return company

    def update(self, instance, validated_data):
        industry_id = validated_data.pop('industry_id', None)
        specializations_ids = validated_data.pop('specializations_ids', None)
        if industry_id is not None:
            from .models import CatalogIndustry
            instance.industry = CatalogIndustry.objects.get(id=industry_id)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if specializations_ids is not None:
            instance.specializations.set(specializations_ids)
        return instance


class MentorProfileSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    company = CompanySerializer(read_only=True)
    company_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    specializations = CatalogFieldSerializer(many=True, read_only=True)
    specializations_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )

    class Meta:
        model = MentorProfile
        fields = [
            'id', 'user_id', 'company', 'company_id',
            'bio', 'experience_years', 'average_rating',
            'skills', 'specializations', 'specializations_ids',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['user_id', 'average_rating', 'created_at', 'updated_at']

    def create(self, validated_data):
        company_id = validated_data.pop('company_id', None)
        specializations_ids = validated_data.pop('specializations_ids', [])
        if company_id:
            from .models import Company
            validated_data['company'] = Company.objects.get(id=company_id)
        mentor = MentorProfile.objects.create(**validated_data)
        if specializations_ids:
            mentor.specializations.set(specializations_ids)
        return mentor

    def update(self, instance, validated_data):
        company_id = validated_data.pop('company_id', None)
        specializations_ids = validated_data.pop('specializations_ids', None)
        if company_id is not None:
            from .models import Company
            instance.company = Company.objects.get(id=company_id)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if specializations_ids is not None:
            instance.specializations.set(specializations_ids)
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request:
            if (hasattr(request.user, 'id') and request.user.id != instance.user_id) and not getattr(request.user, 'is_staff', False):
                representation.pop('bio', None)
        return representation


class MenteeProfileSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    desired_fields = CatalogFieldSerializer(many=True, read_only=True)
    desired_fields_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )

    class Meta:
        model = MenteeProfile
        fields = [
            'id', 'user_id', 'development_goals', 'skills',
            'desired_fields', 'desired_fields_ids',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['user_id', 'created_at', 'updated_at']

    def create(self, validated_data):
        desired_fields_ids = validated_data.pop('desired_fields_ids', [])
        mentee = MenteeProfile.objects.create(**validated_data)
        if desired_fields_ids:
            mentee.desired_fields.set(desired_fields_ids)
        return mentee

    def update(self, instance, validated_data):
        desired_fields_ids = validated_data.pop('desired_fields_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if desired_fields_ids is not None:
            instance.desired_fields.set(desired_fields_ids)
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request:
            if (hasattr(request.user, 'id') and request.user.id != instance.user_id) and not getattr(request.user, 'is_staff', False):
                representation.pop('development_goals', None)
        return representation
