from django.urls import path
from .views import (
    MentorProfileDetail, MenteeProfileDetail, MentorProfileList,
    CompanyList, CatalogIndustryList, CatalogFieldList
)

urlpatterns = [
    # Endpoints for profile views
    path('mentors/<int:pk>/', MentorProfileDetail.as_view(), name='mentor-profile-detail'),  # Get a specific mentor profile
    path('mentees/<int:pk>/', MenteeProfileDetail.as_view(), name='mentee-profile-detail'),  # Get a specific mentee profile
    path('mentors/', MentorProfileList.as_view(), name='mentor-profile-list'),  # List all mentor profiles

    # Endpoints for reference data (catalogs)
    path('companies/', CompanyList.as_view(), name='company-list'),  # List all companies
    path('catalog/industries/', CatalogIndustryList.as_view(), name='catalog-industries-list'),  # List all industries
    path('catalog/fields/', CatalogFieldList.as_view(), name='catalog-fields-list'),  # List all fields
]
