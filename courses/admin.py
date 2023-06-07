from django.contrib import admin
from .models import Courses, ArticleCourse

# Register your models here.


@admin.register(Courses)
class CousesAdmin(admin.ModelAdmin):
    fields = ["title", "bg_color", "image", "published", "modified"]
    list_display = ("title", )
    list_display_links = ("title", )
    list_per_page = 20
    search_fields = ("id", "title")
    readonly_fields = ("published", "modified")


@admin.register(ArticleCourse)
class ArticleCourseAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Header", {"fields": [
         "title", "description", "image", "series", "author"]}),
        ("Content", {"fields": ["content"]}),
        ("Date", {"fields": ["published", "modified"]})
    ]

    list_display = ("title", "series", "author")
    list_display_links = ("title", "series")
    list_filter = ("author", )
    list_per_page = 20
    search_fields = ("title", "id")
    ordering = ("-id", )
    readonly_fields = ("published", "modified")
