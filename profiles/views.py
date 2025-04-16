from django.urls import path
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from .filters import MentorProfileFilter, CompanyFilter, MenteeProfileFilter
from .models import MentorProfile, MenteeProfile, Company, CatalogIndustry, CatalogField
from .serializers import (
    MentorProfileSerializer, MenteeProfileSerializer,
    CompanySerializer, CatalogIndustrySerializer, CatalogFieldSerializer
)
from .permissions import IsOwnerOrAdmin, IsMentorOrAdmin
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView


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

@extend_schema(
    summary="List All Mentee Profiles",
    description="List all mentee profiles with optional filtering by skills, desired_fields, and development_goals. Accessible to mentors and admins.",
    responses={200: MenteeProfileSerializer(many=True), 400: OpenApiResponse(description="Bad Request")},
)
class MenteeProfileSearch(ListAPIView):
    """
    Endpoint for mentors or admins to search mentee profiles.
    """
    queryset = MenteeProfile.objects.all()
    serializer_class = MenteeProfileSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = MenteeProfileFilter
    search_fields = ['development_goals']
    permission_classes = [IsMentorOrAdmin]

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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MentorProfileFilter
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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CompanyFilter
    search_fields = ['name']
    ordering_fields = ['name']
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


@extend_schema_view(
    get=extend_schema(
        summary="Admin: Retrieve Company",
        description="Retrieve a company by ID. Only accessible to admins.",
        responses={
            200: CompanySerializer,
            403: OpenApiResponse(description="Forbidden - Admin access required"),
            404: OpenApiResponse(description="Not Found"),
        },
    ),
    put=extend_schema(
        summary="Admin: Update Company",
        description="Update a company by ID. Only accessible to admins.",
        request=CompanySerializer,
        responses={
            200: CompanySerializer,
            400: OpenApiResponse(description="Bad Request"),
            403: OpenApiResponse(description="Forbidden - Admin access required"),
            404: OpenApiResponse(description="Not Found"),
        },
    ),
    patch=extend_schema(
        summary="Admin: Partially Update Company",
        description="Partially update a company by ID. Only accessible to admins.",
        request=CompanySerializer,
        responses={
            200: CompanySerializer,
            400: OpenApiResponse(description="Bad Request"),
            403: OpenApiResponse(description="Forbidden - Admin access required"),
            404: OpenApiResponse(description="Not Found"),
        },
    ),
    delete=extend_schema(
        summary="Admin: Delete Company",
        description="Delete a company by ID. Only accessible to admins.",
        responses={
            204: OpenApiResponse(description="Deleted successfully"),
            403: OpenApiResponse(description="Forbidden - Admin access required"),
            404: OpenApiResponse(description="Not Found"),
        },
    ),
)
class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Admin-only endpoint to retrieve, update, or delete a company.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAdminUser]


class CompanyAccessValidation(APIView):
    """
    API endpoint for checking if a company access key is valid.
    Accepts JSON:
    {
    "company_id": <int>,
    "access_key": "<raw_key>"
    }
    Returns { "valid": true } or { "valid": false }
    """
    permission_classes = [AllowAny]  # maybe will need a restriction

    def post(self, request):
        company_id = request.data.get("company_id")
        access_key = request.data.get("access_key")
        if not company_id or not access_key:
            return Response({"detail": "company_id and access_key are required."},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            return Response({"detail": "Company not found."},
                            status=status.HTTP_404_NOT_FOUND)
        if company.access_key_hash and check_password(access_key, company.access_key_hash):
            return Response({"valid": True})
        else:
            return Response({"valid": False}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    get=extend_schema(
        summary="Admin: Retrieve Catalog Industry",
        description="Retrieve a catalog industry by ID. Only accessible to admins.",
        responses={
            200: CatalogIndustrySerializer,
            403: OpenApiResponse(description="Forbidden - Admin access required"),
            404: OpenApiResponse(description="Not Found"),
        },
    ),
    put=extend_schema(
        summary="Admin: Update Catalog Industry",
        description="Update a catalog industry by ID. Only accessible to admins.",
        request=CatalogIndustrySerializer,
        responses={
            200: CatalogIndustrySerializer,
            400: OpenApiResponse(description="Bad Request"),
            403: OpenApiResponse(description="Forbidden - Admin access required"),
            404: OpenApiResponse(description="Not Found"),
        },
    ),
    patch=extend_schema(
        summary="Admin: Partially Update Catalog Industry",
        description="Partially update a catalog industry by ID. Only accessible to admins.",
        request=CatalogIndustrySerializer,
        responses={
            200: CatalogIndustrySerializer,
            400: OpenApiResponse(description="Bad Request"),
            403: OpenApiResponse(description="Forbidden - Admin access required"),
            404: OpenApiResponse(description="Not Found"),
        },
    ),
    delete=extend_schema(
        summary="Admin: Delete Catalog Industry",
        description="Delete a catalog industry by ID. Only accessible to admins.",
        responses={
            204: OpenApiResponse(description="Deleted successfully"),
            403: OpenApiResponse(description="Forbidden - Admin access required"),
            404: OpenApiResponse(description="Not Found"),
        },
    ),
)
class CatalogIndustryDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Admin-only endpoint to retrieve, update, or delete a catalog industry.
    """
    queryset = CatalogIndustry.objects.all()
    serializer_class = CatalogIndustrySerializer
    permission_classes = [IsAdminUser]


@extend_schema_view(
    get=extend_schema(
        summary="Admin: Retrieve Catalog Field",
        description="Retrieve a catalog field by ID. Only accessible to admins.",
        responses={
            200: CatalogFieldSerializer,
            403: OpenApiResponse(description="Forbidden - Admin access required"),
            404: OpenApiResponse(description="Not Found"),
        },
    ),
    put=extend_schema(
        summary="Admin: Update Catalog Field",
        description="Update a catalog field by ID. Only accessible to admins.",
        request=CatalogFieldSerializer,
        responses={
            200: CatalogFieldSerializer,
            400: OpenApiResponse(description="Bad Request"),
            403: OpenApiResponse(description="Forbidden - Admin access required"),
            404: OpenApiResponse(description="Not Found"),
        },
    ),
    patch=extend_schema(
        summary="Admin: Partially Update Catalog Field",
        description="Partially update a catalog field by ID. Only accessible to admins.",
        request=CatalogFieldSerializer,
        responses={
            200: CatalogFieldSerializer,
            400: OpenApiResponse(description="Bad Request"),
            403: OpenApiResponse(description="Forbidden - Admin access required"),
            404: OpenApiResponse(description="Not Found"),
        },
    ),
    delete=extend_schema(
        summary="Admin: Delete Catalog Field",
        description="Delete a catalog field by ID. Only accessible to admins.",
        responses={
            204: OpenApiResponse(description="Deleted successfully"),
            403: OpenApiResponse(description="Forbidden - Admin access required"),
            404: OpenApiResponse(description="Not Found"),
        },
    ),
)
class CatalogFieldDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Admin-only endpoint to retrieve, update, or delete a catalog field.
    """
    queryset = CatalogField.objects.all()
    serializer_class = CatalogFieldSerializer
    permission_classes = [IsAdminUser]
