from django.contrib import admin

from reviews.models import Comment, Review, Category, Title, Genre


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "text",
        "author",
        "score",
        "pub_date",
    )
    search_fields = ("text",)
    list_filter = ("pub_date", "title")


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "review",
        "text",
        "author",
        "pub_date",
    )
    search_fields = ("text",)
    list_filter = ("pub_date", "review")


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
    )
    search_fields = ("name",)
    list_filter = ("title", "name")


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
    )
    search_fields = ("name",)
    list_filter = ("title", "name")


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "category",
        "year",
    )
    search_fields = ("name",)
    list_filter = ("name", "category")


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
