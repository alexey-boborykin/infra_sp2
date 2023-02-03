import datetime as dt

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User

from api_yamdb.settings import MAX_VALUE_SLUG


def my_year_validator(value):
    if value < 1 or value > dt.datetime.now().year:
        raise ValidationError("Год не может быть больше текущего")


class Category(models.Model):
    """Категории произведений."""

    name = models.CharField(max_length=256, verbose_name="Название категории")
    slug = models.SlugField(
        max_length=MAX_VALUE_SLUG,
        unique=True,
    )

    class Meta:
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанры."""

    name = models.CharField(max_length=256, verbose_name="Название жанра")
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name_plural = "Жанры"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведения."""

    name = models.CharField(
        max_length=256,
        blank=False,
        null=False,
        verbose_name="Название произведения",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Категории",
    )
    genre = models.ManyToManyField(Genre, verbose_name="Жанры")
    year = models.IntegerField(
        blank=True,
        null=True,
        validators=[my_year_validator],
        verbose_name="Год выпуска",
    )
    description = models.TextField(verbose_name="Описание")

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Review(models.Model):
    """Отзывы."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Произведение",
    )
    text = models.TextField(verbose_name="Текст отзыва")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор",
    )
    score = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10),
        ),
        verbose_name="Рейтинг",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="Дата создания"
    )

    class Meta:
        verbose_name_plural = "Отзывы"
        ordering = ("pub_date",)
        constraints = (
            models.UniqueConstraint(
                fields=("title", "author"),
                name="only_one_review_per_title_from_an_author",
            ),
        )

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Комментарии к отзывам."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Комментарии",
    )
    text = models.TextField(verbose_name="Текст комментария")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="Дата создания"
    )

    class Meta:
        verbose_name_plural = "Комментарии"
        ordering = ("-pub_date",)

    def __str__(self):
        return self.text
