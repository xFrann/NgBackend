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
from django.contrib.auth.models import User
class GetCommentsViewset(NestedViewSetMixin, viewsets.ViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        try:
            announcement_id = self.kwargs.get("parent_lookup_announcements")
            content = request.data['content']
            user = request.data['user']
            user = User.objects.get(username=user)
            Comment.objects.create(announcement_id=announcement_id, user=user, content=content)
            return Response({"success": "data posted"})
        except:
            return Response({"error": "Error when trying to create comment"})

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

    def destroy(self, request, *args, **kwargs):
        try:
            queryset = Comment.objects.filter(announcement_id=self.kwargs.get("parent_lookup_announcements"))
            pk = self.kwargs.get("pk")
            comment = get_object_or_404(queryset, pk=pk)
            if (comment.user != request.user):
                return Response({"error": "You are not allowed to delete this comment"})

            comment.delete()
            return Response({"success": "Comment deleted"})
        except:
            return Response({"error": "Error when trying to delete comment"})
