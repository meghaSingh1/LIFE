from django.urls import path

from . import views

urlpatterns = [
    path('api/check_logged_in', views.check_logged_in, name='check_logged_in'),
    path('api/create_new_post', views.create_new_post, name='create_new_post'),
]