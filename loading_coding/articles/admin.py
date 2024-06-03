from django.contrib import admin
from django.utils.safestring import mark_safe

from articles.models import Posts, Category, Comment, Contact


@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'content', 'photo', 'post_photo', 'cat', 'tags']
    readonly_fields = ('post_photo', )
    prepopulated_fields = {'slug': ('title', )}
    filter_vertical = ('tags', )
    list_display = ('title', 'post_photo', 'time_create', 'is_published', 'cat')
    list_display_links = ('title', )
    ordering = ('-time_create', 'title')
    list_editable = ('is_published', )
    actions = ('set_published', 'set_graft')
    search_fields = ('title__startswith', 'cat__name')
    list_filter = ('cat__name', 'is_published')
    save_on_top = True

    @admin.display(description="Изображение", ordering='content')
    def post_photo(self, posts: Posts):
        if posts.photo:
            return mark_safe(f"<img src='{posts.photo.url}' width=50")
        return "Без фото"

    @admin.action(description="Опубликовать выбранные статьи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Posts.Status.PUBLISHED)
        self.message_user(request, f"Опубликовано {count} статей")

    @admin.action(description="Снять с публикации выбранные статьи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Posts.Status.DRAFT)
        self.message_user(request, f"Снято с публикации {count} статей")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'commenter', 'created', 'updated', 'active')
    list_filter = ('active', 'created', 'updated')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'content', 'viewed', 'created')
    list_display_links = ('id', 'name')
    list_editable = ('viewed', )
    list_filter = ('viewed', 'created')