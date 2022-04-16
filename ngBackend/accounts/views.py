from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet 
from user_profiles.models import UserProfile
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from django.contrib import auth
from .serializer import UserSerializer

class CheckAuthenticatedView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, format=None):
        user = self.request.user

        isAuthenticated = user.is_authenticated
        
        if isAuthenticated:
            return Response({'success': 'User is authenticated'})
        else:
            return Response({'error': 'user not auth'})

@method_decorator(csrf_protect, name='dispatch')
class GetUserView(APIView):
    def get(self, request, format=None):
        user = self.request.user
        user = UserSerializer(user, many=False)
        return Response({'user': user.data})

@method_decorator(csrf_protect, name='dispatch')
class SignupView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        data = self.request.data

        username = data['username']
        password = data['password']
        re_password = data['re_password']

        if password == re_password:
            if User.objects.filter(username=username).exists():
                return Response({'error': 'Username arleady exists'})
            else:
                user = User.objects.create_user(username=username, password=password)
                user = User.objects.get(id=user.id)
                user_profile = UserProfile.objects.create(user=user, first_name='', last_name='', phone='', city='')

                return Response({'success': 'User created'})

@method_decorator(csrf_protect, name='dispatch')
class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        data = self.request.data

        username = data['username']
        password = data['password']
        
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return Response({'success': 'User is authenticated', 'user': username})
        else:
            return Response({'error': 'Error while authenticating'})

class LogoutView(APIView):

    def post(self, request, format=None):
        try:
            auth.logout(request)
            return Response({'success': 'User logged out'})
        except:
            return Response({'error': 'Something went bad'})


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        return Response({'success': 'CSRF cookie set'})


class DeleteAccountView(APIView):
    def delete(self, request, format=None):
        try:
            user = self.request.user
            user = User.objects.filter(id=user.id).delete()
            return Response({'success': 'User deleted'})
        except:
            return Response({'error': 'Something went wrong when trying to delete the user'})


class GetUsersView(ViewSet):
    permission_classes = (permissions.AllowAny, )
    def get(self, request, format=None):
        users = User.objects.all()
        users = UserSerializer(users, many=True)
        return Response(users.data)