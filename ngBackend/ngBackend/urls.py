from django.urls import path, include
from django.contrib import admin
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('accounts/', include('accounts.urls')),
    path('profiles/', include('user_profiles.urls')),
    path('announcements/', include('announcements.urls')),
    path('comments/', include('comments.urls')),
]

# Catch all paths
#urlpatterns +=[re_path(r'^.*', TemplateView.as_view(template_name="index.html"))]