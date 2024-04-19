from django.urls import path
from .views import (ArticleCreate, NewsUpdate, NewsDelete, NewsDetail)


urlpatterns = [
    path('create/', ArticleCreate.as_view(), name='article_create'),
    # path('<int:pk>', NewsDetail.as_view(), name='article_detail'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='article_edit'),
    path('<int:pk>/delete', NewsDelete.as_view(), name='article_delete'),
]
