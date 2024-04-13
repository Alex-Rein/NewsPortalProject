from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


class NewsList(ListView):
    model = Post
    ordering = 'post_time'
    template_name = 'allnews.html'
    context_object_name = 'allnews'


class NewsDetail(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
