from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from api.permissions import IsAdminOrReadOnly, ReviewAndCommentPermission
from api.serializers import (
    CategorySerializers,
    CommentSerializer,
    GenreSerializers,
    ReviewSerializer,
    TitleCRUDSerializers,
    TitleGETSerializers,
)
from api.title_filter import TitleFilter
from reviews.models import Category, Genre, Review, Title


class ActionsViews(
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    pass


class CategoryViewSet(ActionsViews):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (SearchFilter,)
    lookup_field = "slug"
    search_fields = ("name",)


class GenreViewSet(ActionsViews):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializers
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (SearchFilter,)
    lookup_field = "slug"
    search_fields = ("name",)


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg("reviews__score")).all()
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = LimitOffsetPagination
    filterset_class = TitleFilter
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return TitleGETSerializers
        return TitleCRUDSerializers


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (ReviewAndCommentPermission,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (ReviewAndCommentPermission,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review=review)
