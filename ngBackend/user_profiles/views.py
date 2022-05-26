from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from user_profiles.models import UserProfile
from user_profiles.UserProfileSerializer import UserProfileSerializer
from rest_framework.viewsets import ViewSet
class GetUserProfileView(ViewSet):

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'username'

    def list(self, request):
        user = self.request.user
        user = User.objects.get(id=user.id)
        user_profile = UserProfile.objects.all()
        user_profile = UserProfileSerializer(user_profile, many=True)
        return Response({'profile': user_profile.data})

    def retrieve(self, request, username=None):
        user = self.request.user
        user = User.objects.filter(username__iexact=username).first()
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
        user = User.objects.get(id=user.id)
        UserProfile.objects.filter(user=user).update(first_name=first_name, last_name=last_name, phone=phone)
        user_profiles = UserProfile.objects.get(user=user)
        user_profile = UserProfileSerializer(user_profiles)
        return Response({'profile': user_profile.data, 'username': str(user.username)})

