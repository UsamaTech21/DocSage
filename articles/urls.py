from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('my_articles/', views.list_articles, name='list_articles'),
    path('<int:article_id>/', views.article_detail, name='article_detail'),
    path('add/', views.add_article, name='add_article'),
    path('<int:article_id>/edit/', views.edit_article, name='edit_article'),
    path('<int:article_id>/delete/', views.delete_article, name='delete_article'),
    path('<int:article_id>/like/', views.like_article, name='like_article'),
    path('<int:article_id>/comment/', views.add_comment, name='add_comment'),
]

