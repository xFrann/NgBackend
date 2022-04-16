from rest_framework import serializers
from announcements.models import Announcement
from comments.models import Comment

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = "__all__"
