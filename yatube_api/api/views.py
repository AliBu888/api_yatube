import datetime as dt

from .permissions import IsAuthorOrReadOnly
from posts.models import Group, Post
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from .serializers import (CommentsSerializer, GroupSerializer,
                          PostListSerializer)


class PostsViewSet(viewsets.ModelViewSet):
    """ViewSet для получения списка всех постов и создания нового.
    Редактирования и удаления только своего поста."""
    queryset = Post.objects.select_related('author')
    serializer_class = PostListSerializer
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        """Автозаполнение полей author и pub_date"""
        serializer.save(
            author=self.request.user,
        )


class GroupsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentsViewSet(viewsets.ModelViewSet):
    """ViewSet для получения списка всех комментариев и создания нового.
    Редактирования и удаления только своих комментариев."""
    serializer_class = CommentsSerializer
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly,)

    def get_queryset(self):
        """Этот view возвращает комментарии поста с id из запроса."""
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        return post.comments.select_related('author')

    def perform_create(self, serializer):
        """Автозаполнение полей author и created"""
        serializer.save(
            post_id=self.kwargs.get('post_id'),
            author=self.request.user,
            created=dt.date.today()
        )
