from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MentorReviewViewSet, MenteeRatingViewSet

router = DefaultRouter()
router.register(r"reviews", MentorReviewViewSet, basename="mentor-review")
router.register(r"mentee-ratings", MenteeRatingViewSet, basename="mentee-rating")

urlpatterns = [
    path("", include(router.urls)),
]
