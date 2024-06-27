from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Post, Category, Comment, Author


# создаём новый класс для представления товаров в админке
class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    # list_display = [field.name for field in Post._meta.get_fields()]  # генерируем список имён всех полей для
    # более красивого отображения
    list_display = ('id', 'author', 'post_time', 'title', 'short_text', 'categories', 'rating')
    list_filter = ('category', 'author')

    def categories(self, obj):
        return ', '.join([cat.name for cat in obj.category.all()])

    def short_text(self, obj):
        return obj.text if len(obj.text) < 55 else (obj.text[:53] + '..')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'subs')

    def subs(self, obj):
        return ', '.join([sub.username for sub in obj.subscribers.all()])


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'user', 'date', 'rating', 'post')
    list_display_links = ('text', )
    list_filter = ('user', 'post')


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'rating')
    list_display_links = ('user', )


class TransCategoryAdmin(CategoryAdmin, TranslationAdmin):
    model = Category


class TransPostAdmin(PostAdmin, TranslationAdmin):
    model = Post


class TransCommentAdmin(CommentAdmin, TranslationAdmin):
    model = Comment


# Register your models here.
admin.site.register(Post, TransPostAdmin)
admin.site.register(Category, TransCategoryAdmin)
admin.site.register(Comment, TransCommentAdmin)
admin.site.register(Author, AuthorAdmin)
