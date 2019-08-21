from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .models import MyUser, Post
from .serializers import UserSerializer, PostSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import json
from .middlewares import check_user_with_token

from django.db.models import Q
import uuid


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_logged_in(request):
    user_is_valid = check_user_with_token(request)
    if user_is_valid:
        return Response({'message': 'Authorized',}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_new_post(request):
    user_is_valid = check_user_with_token(request)
    data = json.loads(request.body.decode('utf-8'))
    if user_is_valid:
        text_content = data['text_content']
        new_post = Post.objects.create(text_content = text_content, user = request.user)
        return Response({'message': 'Success'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'message': 'Failed'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_feed_posts(request):
    user_is_valid = check_user_with_token(request)
    if user_is_valid:
        user_posts = Post.objects.filter(Q(user = request.user) | Q(user__in=request.user.followings.all())).order_by('-date_created')
        serializer = PostSerializer(user_posts, many = True).data
        return Response({'message': 'Authorized', 'user_posts': serializer}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def check_profile_name_availability(request):
    data = json.loads(request.body.decode('utf-8'))
    request_profile_name = data['profile_name']
    user = MyUser.objects.filter(profile_name = request_profile_name)
    if len(user) == 0:
        return Response({'message': 'Available'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Taken'}, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['POST'])
def user_sign_up(request):
    data = json.loads(request.body.decode('utf-8'))
    email = data['email']
    password = data['password']
    first_name = data['first_name']
    last_name = data['last_name']
    gender = data['gender']
    profile_name = data['profile_name']
    date_of_birth = data['year'] + '-' + data['month'] + '-' + data['date']

    user = MyUser.objects.create(email=email,first_name=first_name,
    last_name=last_name,gender=gender.capitalize(),profile_name=profile_name, date_of_birth=date_of_birth)
    user.set_password(password)
    user.save()
    return Response({'message': 'Available'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def get_user_profile(request):
    data = json.loads(request.body.decode('utf-8'))
    request_profile_name = data['profile_name']
    user = MyUser.objects.filter(profile_name = request_profile_name)
    if len(user) == 1:
        user_serializer = UserSerializer(user[0]).data
        user_posts = Post.objects.filter(user = user[0]).order_by('-date_created')
        is_in_your_following = False
        if data['email'] != -1:
            request_user = MyUser.objects.filter(email = data['email'])
            print(data['email'])
            if len(request_user) == 1:
                if(user[0] in request_user[0].followings.all()):
                    is_in_your_following = True
        post_serializer = PostSerializer(user_posts, many = True).data
        return Response({'message': 'Success', 'user': user_serializer, 'user_posts': post_serializer, 'is_in_your_following': is_in_your_following}, status=status.HTTP_200_OK)
    return Response({'message': 'Failed'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request):
    user_is_valid = check_user_with_token(request)
    data = json.loads(request.body.decode('utf-8'))
    if user_is_valid:
        target_profile_name = data['profile_name']
        target_user = MyUser.objects.filter(profile_name = target_profile_name)
        if len(target_user) == 1:
            if (target_user[0] != request.user):
                if target_user[0] in request.user.followings.all():
                    request.user.followings.remove(target_user[0])
                else:
                    request.user.followings.add(target_user[0])
                request.user.save()
                return Response({'message': 'Success'}, status=status.HTTP_200_OK)
            return Response({'message': 'Failed'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Failed'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'Failed'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_a_post(request):
    user_is_valid = check_user_with_token(request)
    data = json.loads(request.body.decode('utf-8'))
    if user_is_valid:
        print(data)
        target_post_uuid = data['post_uuid']
        target_post = Post.objects.filter(uuid = target_post_uuid)
        if len(target_post) == 1:
            if not request.user in target_post[0].liked_by.all():
                target_post[0].liked_by.add(request.user)
                target_post[0].save()
                return Response({'message': 'Liked'}, status=status.HTTP_200_OK)
            else:
                target_post[0].liked_by.remove(request.user)
                target_post[0].save()
                return Response({'message': 'Unliked'}, status=status.HTTP_200_OK)
        return Response({'message': 'Failed'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'Failed'}, status=status.HTTP_400_BAD_REQUEST)