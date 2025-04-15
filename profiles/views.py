from django.urls import path
from rest_framework import generics, filters
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from .models import MentorProfile, MenteeProfile, Company, CatalogIndustry, CatalogField
from .serializers import (
    MentorProfileSerializer, MenteeProfileSerializer,
    CompanySerializer, CatalogIndustrySerializer, CatalogFieldSerializer
)
from .permissions import IsOwnerOrAdmin


# MentorProfile detail view: Retrieve and update a mentor profile
@extend_schema_view(
    get=extend_schema(
        summary="Retrieve Mentor Profile",
        description="Retrieve a mentor profile by ID. Available to all authenticated users.",
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
        description="Update a mentor profile by ID. Only the profile owner or an admin can perform this action.",
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
        description="Partially update a mentor profile by ID. Only the profile owner or an admin can perform this action.",
        request=MentorProfileSerializer,
        responses={
            200: MentorProfileSerializer,
            400: OpenApiResponse(description="Bad Request - Invalid data"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
            404: OpenApiResponse(description="Not Found"),
        },
    ),
    delete=extend_schema(
        summary="Delete Mentor Profile",
        description="Delete a mentor profile by ID. Only the profile owner or an admin can perform this action.",
        responses={
            204: OpenApiResponse(description="No Content"),
            400: OpenApiResponse(description="Bad Request"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
            404: OpenApiResponse(description="Not Found"),
        },
    ),
)
class MentorProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MentorProfile.objects.all()
    serializer_class = MentorProfileSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsOwnerOrAdmin()]
        return [IsAuthenticated()]

# MenteeProfile detail view: Retrieve and update a mentee profile
@extend_schema_view(
    get=extend_schema(
        summary="Retrieve Mentee Profile",
        description="Retrieve a mentee profile by ID. Available to all authenticated users.",
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
        description="Update a mentee profile by ID. Only the profile owner or an admin can perform this action.",
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
        description="Partially update a mentee profile by ID. Only the profile owner or an admin can perform this action.",
        request=MenteeProfileSerializer,
        responses={
            200: MenteeProfileSerializer,
            400: OpenApiResponse(description="Bad Request - Invalid data"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
            404: OpenApiResponse(description="Not Found"),
        },
    ),
    delete=extend_schema(
        summary="Delete Mentee Profile",
        description="Delete a mentee profile by ID. Only the profile owner or an admin can perform this action.",
        responses={
            204: OpenApiResponse(description="No Content"),
            400: OpenApiResponse(description="Bad Request"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
            404: OpenApiResponse(description="Not Found"),
        },
    ),
)
class MenteeProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenteeProfile.objects.all()
    serializer_class = MenteeProfileSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsOwnerOrAdmin()]
        return [IsAuthenticated()]

# MenteeProfile list view for admin: List all mentee profiles (admin-only)
class MenteeProfileListAdmin(ListAPIView):
    """
    Admin endpoint for viewing all mentee profiles.
    Available only to users with admin rights.
    """
    queryset = MenteeProfile.objects.all()
    serializer_class = MenteeProfileSerializer
    permission_classes = [IsAdminUser]

# MentorProfile list view: List all mentor profiles with filtering and ordering, available to authenticated users
@extend_schema(
    summary="List All Mentor Profiles",
    description="List all mentor profiles with optional filtering by skills, company, experience, etc. Accessible to authenticated users.",
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
    permission_classes = [IsAuthenticated]

# Company list view: List all companies (accessible to authenticated users)
@extend_schema(
    summary="List All Companies",
    description="Retrieve a list of all companies. Accessible to authenticated users.",
    responses={
        200: CompanySerializer(many=True),
        400: OpenApiResponse(description="Bad Request"),
    },
)
class CompanyList(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]
