from django.shortcuts import get_object_or_404      
from rest_framework import viewsets
from announcements.models import Announcement
from rest_framework.response import Response
from announcements.serializers import AnnouncementSerializer
from rest_framework_extensions.mixins import NestedViewSetMixin
class GetAnnouncementsViewSet(NestedViewSetMixin, viewsets.ViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

    def create(self, request):
        data = self.request.data
        user = self.request.user
        try:
            title = data['title']
            content = data['content']
            Announcement.objects.create(user=user, title=title, content=content)
            return Response({"success": "Announcement created succesfully"})
        except KeyError:
            return Response({"error": "Please provide values for title and content"})

    def list(self, request):
        serialize = AnnouncementSerializer(self.queryset, many=True)
        print(serialize.data)
        return Response(serialize.data)

    def retrieve(self, request, pk=None):
        announcement = get_object_or_404(self.queryset, pk=pk)
        serialize = AnnouncementSerializer(announcement)
        return Response(serialize.data)




