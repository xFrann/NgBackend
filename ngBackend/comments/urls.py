from django.urls import path
from comments.views import GetCommentsViewset

def registerPath(router):
    router.register(r'comments', GetCommentsViewset)

def registerNestedPath(router):

    router.register(
        'comments',
        GetCommentsViewset,
        basename='announcements-comments',
        parents_query_lookups=['announcements']
    )

urlpatterns = [

]