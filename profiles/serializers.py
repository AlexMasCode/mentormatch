from rest_framework import serializers
from .models import (
    Company, CatalogIndustry, CatalogField, Skill,
    MentorProfile, MentorSkill, MentorSpecialization,
    MenteeProfile, MenteeSkill, MenteeDesiredField
)


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'description', 'industry', 'logo_url']


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


class MentorProfileSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    company = CompanySerializer(read_only=True)
    company_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = MentorProfile
        fields = [
            'id', 'user_id', 'company', 'company_id',
            'bio', 'experience_years', 'average_rating', 'skills',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['user_id', 'average_rating', 'created_at', 'updated_at']

    def to_representation(self, instance):
        # Return the default representation first
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request:
            # If the request user is not the owner and not an admin, return limited public fields only
            if (hasattr(request.user, 'id') and request.user.id != instance.user_id) and not getattr(request.user, 'is_staff', False):
                # Example: hide sensitive fields for non-owners
                representation.pop('bio', None)
                # You can hide other fields here if needed
        return representation


class MenteeProfileSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = MenteeProfile
        fields = [
            'id', 'user_id', 'development_goals', 'skills',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['user_id', 'created_at', 'updated_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request:
            # If the request user is not the owner and not an admin, hide certain fields
            if (hasattr(request.user, 'id') and request.user.id != instance.user_id) and not getattr(request.user, 'is_staff', False):
                representation.pop('development_goals', None)
        return representation
