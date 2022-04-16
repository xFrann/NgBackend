from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from user_profiles.models import UserProfile
from user_profiles.UserProfileSerializer import UserProfileSerializer

class GetUserProfileView(APIView):
    def get(self, request, format=None):
        user = self.request.user

        user = user.objects.get(id=user.id)
        user_profile = UserProfile.objects.get(user=user)
        user_profile = UserProfileSerializer(user_profile)

        return Response({'profile': user_profile.data, 'username': str(user.username)})


class UpdateUserProfileView(APIView):
    def put(self, request, format=None):
        user = self.request.user
        data = self.request.data
        first_name = data['first_name']
        last_name = data['last_name']
        phone = data['phone']
        city = data['city']
        user = User.objects.get(id=user.id)
        UserProfile.objects.filter(user=user).update(first_name=first_name, last_name=last_name, phone=phone, city=city)
        user_profiles = UserProfile.objects.get(user=user)
        user_profile = UserProfileSerializer(user_profiles)
        return Response({'profile': user_profile.data, 'username': str(user.username)})

