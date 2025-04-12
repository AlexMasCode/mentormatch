from django.urls import path
from rest_framework import generics, filters
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)
from .models import MentorProfile, MenteeProfile, Company, CatalogIndustry, CatalogField
from .serializers import (
    MentorProfileSerializer, MenteeProfileSerializer,
    CompanySerializer, CatalogIndustrySerializer, CatalogFieldSerializer
)
from .permissions import IsOwnerOrAdmin, IsMentor, IsMentee
from rest_framework.permissions import AllowAny

# MentorProfile detail view: Retrieve and update a mentor profile
@extend_schema_view(
    get=extend_schema(
        summary="Retrieve Mentor Profile",
        description="Retrieve a mentor profile by ID. Only the profile owner or an admin can access this endpoint.",
        responses={
            200: MentorProfileSerializer,
            400: OpenApiResponse(description="Bad Request"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
            404: OpenApiResponse(description="Not Found"),
        },
    ),
    put=extend_schema(
        summary="Update Mentor Profile",
        description="Update a mentor profile by ID. All required fields must be provided in the request body.",
        request=MentorProfileSerializer,
        responses={
            200: MentorProfileSerializer,
            400: OpenApiResponse(description="Bad Request - Invalid data"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
            404: OpenApiResponse(description="Not Found"),
        },
    ),
    patch=extend_schema(
        summary="Partially Update Mentor Profile",
        description="Partially update a mentor profile by ID. Only the provided fields will be updated.",
        request=MentorProfileSerializer,
        responses={
            200: MentorProfileSerializer,
            400: OpenApiResponse(description="Bad Request - Invalid data"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
            404: OpenApiResponse(description="Not Found"),
        },
    ),
)
class MentorProfileDetail(generics.RetrieveUpdateAPIView):
    queryset = MentorProfile.objects.all()
    serializer_class = MentorProfileSerializer
    permission_classes = [IsOwnerOrAdmin, IsMentor]


# MenteeProfile detail view: Retrieve and update a mentee profile
@extend_schema_view(
    get=extend_schema(
        summary="Retrieve Mentee Profile",
        description="Retrieve a mentee profile by ID. Only the profile owner or an admin can access this endpoint.",
        responses={
            200: MenteeProfileSerializer,
            400: OpenApiResponse(description="Bad Request"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
            404: OpenApiResponse(description="Not Found"),
        },
    ),
    put=extend_schema(
        summary="Update Mentee Profile",
        description="Update a mentee profile by ID. All required fields must be provided in the request body.",
        request=MenteeProfileSerializer,
        responses={
            200: MenteeProfileSerializer,
            400: OpenApiResponse(description="Bad Request - Invalid data"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
            404: OpenApiResponse(description="Not Found"),
        },
    ),
    patch=extend_schema(
        summary="Partially Update Mentee Profile",
        description="Partially update a mentee profile by ID. Only the provided fields will be updated.",
        request=MenteeProfileSerializer,
        responses={
            200: MenteeProfileSerializer,
            400: OpenApiResponse(description="Bad Request - Invalid data"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
            404: OpenApiResponse(description="Not Found"),
        },
    ),
)
class MenteeProfileDetail(generics.RetrieveUpdateAPIView):
    queryset = MenteeProfile.objects.all()
    serializer_class = MenteeProfileSerializer
    permission_classes = [IsOwnerOrAdmin, IsMentee]


# MentorProfile list view: List all mentor profiles with filtering and ordering
@extend_schema(
    summary="List All Mentor Profiles",
    description="List all mentor profiles with optional filtering by skills, company, experience, etc.",
    responses={
        200: MentorProfileSerializer(many=True),
        400: OpenApiResponse(description="Bad Request"),
    },
)
class MentorProfileList(generics.ListAPIView):
    serializer_class = MentorProfileSerializer
    queryset = MentorProfile.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['bio', 'company__name']
    ordering_fields = ['experience_years', 'average_rating']


# Company list view: List all companies (public access)
@extend_schema(
    summary="List All Companies",
    description="Retrieve a list of all companies. This endpoint is public.",
    responses={
        200: CompanySerializer(many=True),
        400: OpenApiResponse(description="Bad Request"),
    },
)
class CompanyList(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [AllowAny]


# CatalogIndustry list view: List all catalog industries (public access)
@extend_schema(
    summary="List All Catalog Industries",
    description="Retrieve a list of all catalog industries. This endpoint is public.",
    responses={
        200: CatalogIndustrySerializer(many=True),
        400: OpenApiResponse(description="Bad Request"),
    },
)
class CatalogIndustryList(generics.ListAPIView):
    queryset = CatalogIndustry.objects.all()
    serializer_class = CatalogIndustrySerializer
    permission_classes = [AllowAny]


# CatalogField list view: List all catalog fields (public access)
@extend_schema(
    summary="List All Catalog Fields",
    description="Retrieve a list of all catalog fields. This endpoint is public.",
    responses={
        200: CatalogFieldSerializer(many=True),
        400: OpenApiResponse(description="Bad Request"),
    },
)
class CatalogFieldList(generics.ListAPIView):
    queryset = CatalogField.objects.all()
    serializer_class = CatalogFieldSerializer
    permission_classes = [AllowAny]


# URL patterns for the profile service endpoints
urlpatterns = [
    # Endpoints for profile views
    path('mentors/<int:pk>/', MentorProfileDetail.as_view(), name='mentor-profile-detail'),
    path('mentees/<int:pk>/', MenteeProfileDetail.as_view(), name='mentee-profile-detail'),
    path('mentors/', MentorProfileList.as_view(), name='mentor-profile-list'),

    # Endpoints for reference data (catalogs)
    path('companies/', CompanyList.as_view(), name='company-list'),
    path('catalog/industries/', CatalogIndustryList.as_view(), name='catalog-industries-list'),
    path('catalog/fields/', CatalogFieldList.as_view(), name='catalog-fields-list'),
]
