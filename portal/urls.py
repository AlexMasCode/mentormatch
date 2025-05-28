# portal/urls.py
from django.urls import path
from . import views, stubs

app_name = "portal"
urlpatterns = [
    path("",         views.HomeView.as_view(),   name="home"),
    path('mentee/home/', views.MenteeHomeView.as_view(), name='mentee_home'),
    path('mentor/home/', views.MentorHomeView.as_view(), name='mentor_home'),

    path("login/",   views.LoginView.as_view(),  name="login"),
    path("logout/",  stubs.logout_view,          name="logout"),
    path("register/",views.RegisterView.as_view(), name="register"),
    path('mentor/fields/', views.MentorFieldSelectionView.as_view(), name='mentor_fields'),

    path("availability/new/", stubs.create_availability, name="create_availability"),
    path("mentor/reviews/",   stubs.mentor_reviews,      name="mentor_reviews"),

    path("mentors/find/",     stubs.find_mentor,         name="find_mentor"),
    path("mentors/<int:mentor_id>/", stubs.view_mentor_profile, name="mentor_profile"),
    path("feedback/new/",     stubs.give_feedback,       name="give_feedback"),

    path("sessions/",         stubs.sessions,            name="sessions"),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
