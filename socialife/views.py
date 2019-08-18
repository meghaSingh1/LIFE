from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .models import MyUser, Post
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import json

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_logged_in(request):
    if request.method == 'POST':
        user_email = request.user.email
        data = json.loads(request.body.decode('utf-8'))
        request_email = data['email']
        if user_email == request_email:
                return Response({'message': 'Authorized'}, status=status.HTTP_200_OK)
        else:
                return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_new_post(request):
    if request.method == 'POST':
        user_email = request.user.email
        data = json.loads(request.body.decode('utf-8'))
        request_email = data['email']
        if user_email == request_email:
                text_content = data['text_content']
                new_post = Post.objects.create(text_content = text_content, user = request.user)
                return Response({'message': 'Success'}, status=status.HTTP_201_CREATED)
        else:
                return Response({'message': 'Failed'}, status=status.HTTP_400_BAD_REQUEST)
