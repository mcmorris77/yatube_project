from django.urls import path, include
from . import views 

app_name = 'posts'

urlpatterns = [
    path('', views.index, name='main'),
    path('group/<slug:slug>/', views.group_posts, name='group_list'),
    path('auth/', include('django.contrib.auth.urls'))
]
