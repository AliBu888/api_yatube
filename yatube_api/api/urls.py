from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import SimpleRouter

from .views import CommentsViewSet, GroupsViewSet, PostsViewSet

router = SimpleRouter()
router.register('posts', PostsViewSet)
router.register('groups', GroupsViewSet)
router.register(
    r'posts/(?P<post_id>[^/.]+)/comments',
    CommentsViewSet,
    basename='comments'
)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
]
