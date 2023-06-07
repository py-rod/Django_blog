from django.db import models
from django.contrib.auth import get_user_model
from colorfield.fields import ColorField
from tinymce.models import HTMLField
from django.utils import timezone
from django.template.defaultfilters import slugify
import os
import random
import string
# Create your models here.


class Courses(models.Model):
    def image_upload_to(self, instance):
        if instance:
            return os.path.join("Courses", slugify(self.slug), instance)
        return None

    title = models.CharField(max_length=100, default="",
                             blank=False, unique=True)
    slug = models.SlugField(default="", blank=False, unique=True, null=False)
    author = models.ForeignKey(
        get_user_model(), default=1, on_delete=models.SET_DEFAULT)
    bg_color = ColorField("Choise Color", default="#FFFFFF",
                          blank=True, help_text="Select color for background image")
    image = models.ImageField(
        default="./default/noimage_curso.png", upload_to=image_upload_to, max_length=255)
    published = models.DateTimeField("Published", default=timezone.now)
    modified = models.DateTimeField("Modified", default=timezone.now)

    # SLUG AUTOMATICO
    def save(self, *args, **kwargs):
        slug_random = "".join(random.sample(
            f"{string.ascii_lowercase}{string.ascii_uppercase}", 50))

        while True:
            if Courses.objects.filter(slug=slug_random).exists() == False and self.slug == "":
                print("no existe este slug")
                self.slug = slug_random
                super(Courses, self).save(*args, **kwargs)
                break
            elif Courses.objects.filter(slug=self.slug).exists() == True and self.slug != "":
                print("Guardando el mismo slug")
                super(Courses, self).save(*args, **kwargs)
                break
            else:
                slug_random = "".join(random.sample(
                    f"{string.ascii_lowercase}{string.ascii_uppercase}", 50))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Courses"
        db_table = "Couses"
        ordering = ("-id", )


class ArticleCourse (models.Model):
    def image_upload_to(self, instance):
        if instance:
            return os.path.join("ArticleCourse", slugify(self.series.slug), slugify(self.article_slug), instance)
        return None

    title = models.CharField(max_length=200, default="",
                             blank=False, unique=False)
    description = models.CharField(max_length=600,
                                   verbose_name="Description", default="", blank=True, unique=False)
    image = models.ImageField(
        default="./default/noimage_curso.png", upload_to=image_upload_to, max_length=255)
    author = models.ForeignKey(
        get_user_model(), default=1, on_delete=models.CASCADE)
    article_slug = models.SlugField(
        "Article Slug", default="", blank=False, unique=True, null=False)
    series = models.ForeignKey(
        Courses, default="", help_text="Select course for create article", on_delete=models.SET_DEFAULT)
    content = HTMLField(default="", blank=True, unique=False)
    published = models.DateTimeField("Date Published", default=timezone.now)
    modified = models.DateTimeField("Date Modified", default=timezone.now)

    # SLUG AUTOMATICO
    def save(self, *args, **kwargs):
        slug_random = "".join(random.sample(
            f"{string.ascii_lowercase}{string.ascii_uppercase}", 50))

        while True:
            if ArticleCourse.objects.filter(article_slug=slug_random).exists() == False and self.article_slug == "":
                print("no existe este slug y es esta recien creado")
                self.article_slug = slug_random
                super(ArticleCourse, self).save(*args, **kwargs)
                break
            elif ArticleCourse.objects.filter(article_slug=self.article_slug).exists() == True and self.article_slug != "":
                print("estamos guardando el mismo slug")
                super(ArticleCourse, self).save(*args, **kwargs)
                break
            else:
                slug_random = "".join(random.sample(
                    f"{string.ascii_lowercase}{string.ascii_uppercase}", 50))

    def __str__(self):
        return self.title

    def slug(self):
        return self.series.slug + "/" + self.article_slug

    class Meta:
        verbose_name_plural = "Articles"
        db_table = "Articles"
        ordering = ("-id", )
