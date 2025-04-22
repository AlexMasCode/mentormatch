from django.urls import path
from .views import (
    MentorProfileDetail, MenteeProfileDetail, MentorProfileList,
    CompanyList, CatalogIndustryList, CatalogFieldList, MenteeProfileListAdmin,
    CompanyDetail, CatalogIndustryDetail, CatalogFieldDetail, CompanyAccessValidation,
    MenteeProfileSearch, MenteeProfileMe
)

urlpatterns = [
    # Endpoints for profile views
    path('mentors/<int:pk>/', MentorProfileDetail.as_view(), name='mentor-profile-detail'),  # Get a specific mentor profile
    path('mentees/<int:pk>/', MenteeProfileDetail.as_view(), name='mentee-profile-detail'),  # Get a specific mentee profile
    path('mentors/', MentorProfileList.as_view(), name='mentor-profile-list'),  # List all mentor profiles
    path('admin/mentees/', MenteeProfileListAdmin.as_view(), name='mentee-list-admin'),

    path('mentees/search/', MenteeProfileSearch.as_view(), name='mentee-search'),


    path('mentees/me/', MenteeProfileMe.as_view(), name='mentee-profile-me'),
    # Endpoints for reference data (catalogs)
    path('companies/', CompanyList.as_view(), name='company-list'),  # List all companies
    path('catalog/industries/', CatalogIndustryList.as_view(), name='catalog-industries-list'),  # List all industries
    path('catalog/fields/', CatalogFieldList.as_view(), name='catalog-fields-list'),  # List all fields

    path('companies/<int:pk>/', CompanyDetail.as_view(), name='company-detail'),
    path('catalog/industries/<int:pk>/', CatalogIndustryDetail.as_view(), name='catalog-industry-detail'),
    path('catalog/fields/<int:pk>/', CatalogFieldDetail.as_view(), name='catalog-field-detail'),

    path('companies/validate-access/', CompanyAccessValidation.as_view(), name='company-access-validation'),
]
