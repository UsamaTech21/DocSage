from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('join_as_doctor/', views.join_as_doctor, name='join_as_doctor'),
    path('reviews/add/', views.add_review, name='add_review'),
    path('reviews/', views.review_list, name='review_list'),
    path('inbox/', views.inbox, name='inbox'),
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('start_conversation/<int:user_id>/', views.start_conversation, name='start_conversation'),
    path('conversation/<int:conversation_id>/send_message/', views.send_message, name='send_message'),
    path('search_users/', views.search_users, name='search_users'),
]
