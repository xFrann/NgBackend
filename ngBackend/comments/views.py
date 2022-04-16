from django.shortcuts import render
from rest_framework.views import APIView
from comments.models import Comment
from announcements.models import Announcement
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import viewsets
from announcements.models import Announcement
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin
from comments.serializers import CommentSerializer
from rest_framework.exceptions import PermissionDenied

class GetCommentsViewset(NestedViewSetMixin, viewsets.ViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            try:
                announcement_id = self.kwargs.get("parent_lookup_announcements")
                content = request.data['content']
                Comment.objects.create(announcement_id=announcement_id, user=self.request.user, content=content)
                return Response({"success": "data posted"})
            except:
                return Response({"error": "Error when trying to create comment"})
        else:
            raise PermissionDenied({"error": "You are not authorized to post to this endpoint."})

    def list(self, request, *args, **kwargs):
        queryset = Comment.objects.filter(announcement_id=self.kwargs.get("parent_lookup_announcements"))
        serialize = CommentSerializer(queryset, many=True)
        return Response(serialize.data)

    def retrieve(self, request, *args, **kwargs):
        queryset = Comment.objects.filter(announcement_id=self.kwargs.get("parent_lookup_announcements"))
        pk = self.kwargs.get("pk")
        comment = get_object_or_404(queryset, pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
