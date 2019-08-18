from django.urls import path

from . import views

urlpatterns = [
    path('api/check_logged_in', views.check_logged_in, name='check_logged_in'),
    path('api/create_new_post', views.create_new_post, name='create_new_post'),
    path('api/get_user_posts', views.get_user_posts, name='get_user_posts'),
]