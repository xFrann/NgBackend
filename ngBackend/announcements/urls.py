# pylint: disable=reportMissingImport
from django.urls import re_path
from django.conf.urls import include
from announcements.views import GetAnnouncementsViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import NestedRouterMixin #nolint
from comments.urls import registerNestedPath

router = DefaultRouter()
router.register(r'', GetAnnouncementsViewSet)
class NestedDefaultRouter(NestedRouterMixin, DefaultRouter):
    pass

router = NestedDefaultRouter()

announcement_router = router.register('', GetAnnouncementsViewSet)
registerNestedPath(announcement_router)

urlpatterns = [
    re_path(r'', include(router.urls))

]