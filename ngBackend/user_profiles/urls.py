

from django.urls import path
from user_profiles.views import GetUserProfileView, UpdateUserProfileView

urlpatterns = [
    path('user', GetUserProfileView.as_view()),
    path('update', UpdateUserProfileView.as_view()),

]