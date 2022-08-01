from math import perm
from django.contrib.auth.models import User
from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from accounts.models import InviteCode 
from user_profiles.models import UserProfile
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from django.contrib import auth
from .serializer import UserSerializer
from rest_framework.parsers import FormParser, MultiPartParser
from django.core.validators import validate_email
from django.core.mail import send_mail
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

#@method_decorator(csrf_protect, name='dispatch')
class SignupView(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = [FormParser, MultiPartParser]

    def validate_image(self, file):
        if file == None:
            raise ValidationError('Invalid Image uploaded')
        if file.size > 5242880:
            raise ValidationError('File too large ( > 5mb )')
        if file.content_type not in ['image/jpeg', 'image/png', 'image/gif']:
            raise ValidationError('File type not supported')


    def post(self, request, format=None):
        data = request.data
        username = data['username']
        password = data['password']
        re_password = data['re_password']
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        phone = data['phone']
        file = data.get('file')

        try:
            self.validate_image(file)
        except ValidationError as error:
            return Response({'error': str(error)})

        try:
            email = validate_email(email)
        except ValidationError:
            return Response({'error': 'Error when validating email on signup'})

        if password != re_password:
            return Response({'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username arleady exists'})
        
        user = User.objects.create_user(username=username, password=password, email=email)
        user = User.objects.get(id=user.id)
        UserProfile.objects.create(user=user, first_name=first_name, last_name=last_name, phone=phone, picture=file)
        return Response({'success': 'User created'})


@method_decorator(csrf_protect, name='dispatch')
class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        data = self.request.data

        username = data['username']
        password = data['password']
        try:
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return Response({'success': 'User is authenticated', 'user': username})
            else:
                return Response({'error': 'Invalid credentials'}, status=401)
        except:
            return Response({'error': 'Internal error while authenticating'}, status=500)


class LogoutView(APIView):
    def post(self, request, format=None):
        try:
            auth.logout(request)
            return Response({'success': 'User logged out'})
        except:
            return Response({'error': 'Internal error while logging out'}, status=500)


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
            return Response({'error': 'Internal error when trying to delete the user'}, status=500)


class GetUsersView(ViewSet):
    permission_classes = (permissions.AllowAny, )
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def list(self, request, format=None):
        users = User.objects.all()
        users = UserSerializer(users, many=True)
        return Response(users.data)

class GetInviteCodePost(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        try:
            data = self.request.data
            invite_code = data['code']
            if InviteCode.objects.filter(code=invite_code).exists():
                return Response({'success': 'Invite code is valid'})
            else:
                return Response({'error': 'Invite code is not valid'}, status=401)
        except:
            return Response({'error': 'Internal error when trying to validate the invite code'}, status=500)

class GetUserExists(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        try:
            data = self.request.data
            username = data['username']
            if User.objects.filter(username=username).exists():
                return Response({'success': 'User already Exists'})
            else:
                return Response({'error': 'User does not exist'})
        except:
            return Response({'error': 'Internal error when trying to verify user'}, status=500)

class GetEmailExists(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        try:
            data = self.request.data
            email = data['email']
            if User.objects.filter(email=email).exists():
                return Response({'success': 'Email already Exists'})
            else:
                return Response({'error': 'Email does not exist'})
        except:
            return Response({'error': 'Internal error when trying to verify email'}, status=500)

class SendTestEmail(APIView):
    permission_classes = (permissions.AllowAny, )
    
    def post(self, request, format=None):
        send_mail('Test Email', 'This is a test email', 'contact@frann.dev', ['frangumada@gmail.com'], fail_silently=False,)