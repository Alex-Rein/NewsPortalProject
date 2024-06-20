from django.urls import path
from .views import (NewsList, NewsDetail, PostSearch,
                    NewsCreate, NewsUpdate, NewsDelete,
                    upgrade_me, subscribe, CategoryListView)
from django.views.decorators.cache import cache_page


#  Ссылки начинаются с /news/
urlpatterns = [
    path('', cache_page(60)(NewsList.as_view()), name='news_list'),
    path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
    # path('<int:pk>', cache_page(60*5)(NewsDetail.as_view()), name='news_detail'),  # кэш дженерик вьюхи на 5 мин
    path('search/', PostSearch.as_view(), name='post_search'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
    path('<int:pk>/delete', NewsDelete.as_view(), name='news_delete'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe/', subscribe, name='subscribe'),
]
