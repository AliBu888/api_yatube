import datetime as dt

from django.core.exceptions import PermissionDenied
from posts.models import Comment, Group, Post
from rest_framework import viewsets

from .serializers import (CommentsSerializer, GroupSerializer,
                          PostListSerializer)


class PostsViewSet(viewsets.ModelViewSet):
    """ViewSet для получения списка всех постов и создания нового.
    Редактирования и удаления только своего поста."""
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

    def perform_create(self, serializer):
        """Автозаполнение полей author и pub_date"""
        serializer.save(
            author=self.request.user,
            pub_date=dt.date.today()
        )

    def perform_update(self, serializer):
        """Запрет на изменение чужого поста."""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied
        super(PostsViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer):
        """Запрет на удаление чужого поста."""
        if serializer.author != self.request.user:
            raise PermissionDenied
        super(PostsViewSet, self).perform_destroy(serializer)


class GroupsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentsViewSet(viewsets.ModelViewSet):
    """ViewSet для получения списка всех комментариев и создания нового.
    Редактирования и удаления только своих комментариев."""
    serializer_class = CommentsSerializer

    def get_queryset(self):
        """Этот view возвращает комментарии поста с id из запроса."""
        return Comment.objects.filter(post__id=self.kwargs['post_id'])

    def perform_create(self, serializer):
        """Автозаполнение полей author и created"""
        serializer.save(
            post=Post.objects.get(id=self.kwargs['post_id']),
            author=self.request.user,
            created=dt.date.today()
        )

    def perform_update(self, serializer):
        """Запрет на изменение чужого комментраия."""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied
        super(CommentsViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer):
        """Запрет на удаление чужого комментраия."""
        if serializer.author != self.request.user:
            raise PermissionDenied
        super(CommentsViewSet, self).perform_destroy(serializer)
