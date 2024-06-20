from django.contrib import admin
from .models import Post, Category


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


# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
