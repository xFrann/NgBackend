from django.urls import path, re_path
from django.conf.urls import include
from announcements.views import CreateAnnoucementView, GetAnnouncementsViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import NestedRouterMixin

from comments.urls import registerPath, registerNestedPath

router = DefaultRouter()
router.register(r'', GetAnnouncementsViewSet)
class NestedDefaultRouter(NestedRouterMixin, DefaultRouter):
    pass

router = NestedDefaultRouter()

announcement_router = router.register('', GetAnnouncementsViewSet)
registerNestedPath(announcement_router)

urlpatterns = [
    path('create', CreateAnnoucementView.as_view()),
    re_path(r'', include(router.urls))

]