from django.urls import path, include
from .views import GetEmailExists, GetUserExists, GetUserView, SendTestEmail, SignupView, GetCSRFToken, LoginView, LogoutView, CheckAuthenticatedView, DeleteAccountView, GetUsersView, GetInviteCodePost
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', GetUsersView, basename="users")

urlpatterns = [
    path('', include(router.urls)),
    path('register', SignupView.as_view()),
    path('csrf_cookie', GetCSRFToken.as_view()),
    path('authenticated', CheckAuthenticatedView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('delete', DeleteAccountView.as_view()),
    path('get_user', GetUserView.as_view()),
    path('code', GetInviteCodePost.as_view()),
    path('user_exists', GetUserExists.as_view()),
    path('email_exists', GetEmailExists.as_view()),
    path('sendmail', SendTestEmail.as_view()),
]
