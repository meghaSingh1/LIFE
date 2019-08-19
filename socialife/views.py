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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_logged_in(request):
    user_is_valid = check_user_with_token(request)
    if user_is_valid:
        return Response({'message': 'Authorized'}, status=status.HTTP_200_OK)
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
def get_user_posts(request):
    user_is_valid = check_user_with_token(request)
    if user_is_valid:
        user_posts = Post.objects.filter(user = request.user).order_by('-date_created')
        serializer = PostSerializer(user_posts, many = True).data
        print(serializer)
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



