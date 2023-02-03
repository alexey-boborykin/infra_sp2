from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title

from api_yamdb.settings import MAX_VALUE_SLUG

MIN_SCORE = 1
MAX_SCORE = 10


class CategorySerializers(serializers.ModelSerializer):
    def validate_slug(self, value):
        if len(value) > MAX_VALUE_SLUG:
            raise serializers.ValidationError(
                "Длина slug категории превышает допустимых 50 символов"
            )
        return value

    class Meta:
        model = Category
        fields = ["name", "slug"]


class GenreSerializers(serializers.ModelSerializer):
    def validate_slug(self, value):
        if len(value) > MAX_VALUE_SLUG:
            raise serializers.ValidationError(
                "Длина slug жанра превышает допустимых 50 символов"
            )
        return value

    class Meta:
        model = Genre
        fields = ["name", "slug"]


class TitleGETSerializers(serializers.ModelSerializer):
    category = CategorySerializers(many=False, read_only=True)
    genre = GenreSerializers(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = "__all__"


class TitleCRUDSerializers(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="slug", read_only=False, queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field="slug",
        read_only=False,
        queryset=Genre.objects.all(),
        many=True,
    )

    class Meta:
        model = Title
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(slug_field="name", read_only=True)
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )

    def validate_score(self, value):
        if MIN_SCORE > value > MAX_SCORE:
            raise serializers.ValidationError("Допустимые значения: 1 - 10")
        return value

    def validate(self, data):
        if self.context.get("request").method == "POST":
            title = get_object_or_404(
                Title, pk=self.context.get("view").kwargs.get("title_id")
            )
            if Review.objects.filter(
                title=title, author=self.context.get("request").user
            ).exists():
                raise serializers.ValidationError(
                    "Вы можете оставить только один отзыв на это произведение."
                )
        return data

    class Meta:
        fields = "__all__"
        model = Review
        read_only_fields = (
            "title",
            "author",
            "pub_date",
        )


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(slug_field="text", read_only=True)
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = "__all__"
        model = Comment
        read_only_fields = (
            "review",
            "author",
            "pub_date",
        )
