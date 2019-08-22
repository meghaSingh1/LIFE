from django.urls import path

from . import views

urlpatterns = [
    path('api/user_sign_up', views.user_sign_up, name='user_sign_up'),
    path('api/check_logged_in', views.check_logged_in, name='check_logged_in'),
    path('api/create_new_post', views.create_new_post, name='create_new_post'),
    path('api/like_a_post', views.like_a_post, name='like_a_post'),
    path('api/add_a_comment', views.add_a_comment, name='add_a_comment'),
    path('api/follow_user', views.follow_user, name='follow_user'),
    path('api/get_feed_posts', views.get_feed_posts, name='get_feed_posts'),
    path('api/get_user_profile', views.get_user_profile, name='get_user_profile'),
    path('api/check_profile_name_availability', views.check_profile_name_availability, name='check_profile_name_availability'),
]