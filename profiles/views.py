from rest_framework import generics, filters
from .models import MentorProfile, MenteeProfile, Company, CatalogIndustry, CatalogField
from .serializers import (
    MentorProfileSerializer, MenteeProfileSerializer,
    CompanySerializer, CatalogIndustrySerializer, CatalogFieldSerializer
)
from .permissions import IsOwnerOrAdmin
from rest_framework.permissions import AllowAny

# Retrieve and update a mentor profile (only for the owner or admin)
class MentorProfileDetail(generics.RetrieveUpdateAPIView):
    queryset = MentorProfile.objects.all()
    serializer_class = MentorProfileSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_object(self):
        # Assumes pk is the profile ID (user_id is stored in the model)
        return super().get_object()

# Retrieve and update a mentee profile (only for the owner or admin)
class MenteeProfileDetail(generics.RetrieveUpdateAPIView):
    queryset = MenteeProfile.objects.all()
    serializer_class = MenteeProfileSerializer
    permission_classes = [IsOwnerOrAdmin]

# List all mentors, with optional filtering by skill, company, experience, etc.
class MentorProfileList(generics.ListAPIView):
    serializer_class = MentorProfileSerializer
    queryset = MentorProfile.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['bio', 'company__name']  # Can be extended as needed
    ordering_fields = ['experience_years', 'average_rating']

# List of all companies (public access)
class CompanyList(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [AllowAny]

# List of all catalog industries (public access)
class CatalogIndustryList(generics.ListAPIView):
    queryset = CatalogIndustry.objects.all()
    serializer_class = CatalogIndustrySerializer
    permission_classes = [AllowAny]

# List of all catalog fields (public access)
class CatalogFieldList(generics.ListAPIView):
    queryset = CatalogField.objects.all()
    serializer_class = CatalogFieldSerializer
    permission_classes = [AllowAny]
