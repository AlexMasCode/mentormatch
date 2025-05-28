from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AvailabilityViewSet, SessionViewSet

router = DefaultRouter()
router.register(r'availability', AvailabilityViewSet, basename='availability')
router.register(r'sessions', SessionViewSet, basename='session')

urlpatterns = [
    path('', include(router.urls)),
]