from django.core.cache import cache
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse

from django.utils.translation import gettext as _
from django.utils.translation import pgettext_lazy # импортируем «ленивый» геттекст с подсказкой


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = self.post_set.aggregate(pr=Coalesce(Sum('rating'), 0))['pr']
        comments_rating = self.user.comment_set.aggregate(cr=Coalesce(Sum('rating'), 0))['cr']
        posts_comments_rating = self.post_set.aggregate(pcr=Coalesce(Sum('comment__rating'), 0))['pcr']

        self.rating = posts_rating * 3 + comments_rating + posts_comments_rating
        self.save()

    def __str__(self):
        return f'{self.user.username}'


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text=_('category name'))  # добавим переводящийся
    # текст подсказку к полю)
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories')

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    article = 'AR'
    news = 'NE'

    POSITIONS = [
        (article, 'Статья'),
        (news, 'Новости'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    news_type = models.CharField(max_length=2, choices=POSITIONS, default=article)
    post_time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    category = models.ManyToManyField(
        Category,
        through='PostCategory',
        verbose_name=pgettext_lazy('help text for MyModel model', 'This is the help text'),
    )

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124]+'...'

    def __str__(self):  # настройка отображения на страницах
        return f'{self.title.title()} {self.text[:20]}'

    def get_absolute_url(self):  # абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return reverse('news_detail', args=[str(self.id)])

    # def get_absolute_url(self):
    #     return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
