from django.contrib import admin

from .models import Article, ArticleScope, Tag


class RelationshipInline(admin.TabularInline):
    model = ArticleScope


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [RelationshipInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass