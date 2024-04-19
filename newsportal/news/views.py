from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView, DeleteView)

from .models import Post
from .filters import PostFilter
from .forms import PostForm


class NewsList(ListView):
    model = Post
    ordering = 'post_time'
    template_name = 'allnews.html'
    context_object_name = 'allnews'
    paginate_by = 10


class NewsDetail(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'


class NewsCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'

    def from_valid(self, form):
        post = form.save(commit=False)
        post.news_type = 'NE'
        return super().form_valid(form)


class NewsUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'


class NewsDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')


class ArticleCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'

    def from_valid(self, form):
        post = form.save(commit=False)
        post.news_type = 'AR'
        return super().form_valid(form)


class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    ordering = '-post_time'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        if self.request.GET:
            return self.filterset.qs
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

