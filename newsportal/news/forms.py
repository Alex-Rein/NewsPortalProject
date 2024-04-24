from django import forms
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


from .models import Post, Category, Author


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=200, label='Заголовок')
    text = forms.CharField(widget=forms.Textarea, label='Текст')
    category = forms.ChoiceField(
        choices=Category.objects.all().values_list(),
        label='Категория')
    author = forms.ModelChoiceField(
        # choices=Author.objects.all().values_list('id', 'user__username'),
        queryset=Author.objects.all(), label='Автор')

    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'category',
            'author',
        ]

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
