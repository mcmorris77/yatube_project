from django.urls import path, include
from . import views 

app_name = 'posts'

urlpatterns = [
    path('', views.index, name='main'),
    path('group/<slug:slug>/', views.group_posts, name='group_list'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('create/', views.post_create, name='post_create'),
    path('posts/<int:pk>/edit', views.post_edit, name='post_edit'),
    path('auth/', include('django.contrib.auth.urls'))
]
