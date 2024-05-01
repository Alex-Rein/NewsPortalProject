import datetime

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Category, Author


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=200, label='Заголовок')
    text = forms.CharField(widget=forms.Textarea, label='Текст')
    category = forms.ChoiceField(
        choices=Category.objects.all().values_list(),
        label='Категория')
    author = forms.ModelChoiceField(
        queryset=Author.objects.all(), label='Автор', empty_label=None)

    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'category',
            'author',
        ]

# """Второй вариант ограничения на посты с выводом ошибки сразу в форме"""
    # def clean(self):
    #     cleaned_data = super().clean()
    #     author = cleaned_data['author']
    #     today = datetime.date.today()
    #     post_limit = Post.objects.filter(author=author, post_time__date=today).count()
    #     if post_limit >= 3:
    #         raise ValidationError('Ограничение на 3 поста в сутки')
    #     return cleaned_data

    def clean_title(self):
        title = self.cleaned_data['title']
        if title[0].islower():
            raise ValidationError(
                'Заголовок должен начинаться с большой буквы.'
            )
        return title


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user
