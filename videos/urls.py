from django.urls import path
from . import views

app_name = 'videos'

urlpatterns = [
    path('', views.home, name='home'),
    path('video/<int:video_id>/', views.video_player, name='video_player'),
    path('category/<int:category_id>/', views.video_list, name='video_list'),
    path('category/<int:category_id>/subcategory/<int:subcategory_id>/', views.video_list, name='video_list'),
    path('category/', views.video_list, {'category_id': None}, name='video_list_all'),
    path('upload/', views.upload_video, name='upload_video'),
]
