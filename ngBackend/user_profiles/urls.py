from django.db import router
from django.urls import path, include
from user_profiles.views import GetUserProfileView, UpdateUserProfileView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'user', GetUserProfileView, basename="user_profile")

urlpatterns = [
    path('', include(router.urls)),
    path('update', UpdateUserProfileView.as_view()),
]