from .models import MyUser, Post
from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['email'] = self.user.email
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        data['gender'] = self.user.gender
        data['profile_name'] = self.user.profile_name
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class UserSerializer(serializers.ModelSerializer):
    # followings = RecursiveField(many = True)
    class Meta:
        model = MyUser
        fields = ['email', 'first_name', 'last_name', 'profile_name', 'get_followings']

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    liked_by = UserSerializer(many = True)
    date_created = serializers.DateTimeField('%B %d %Y at %H:%M')
    class Meta:
        model = Post
        fields = ['user', 'text_content', 'date_created', 'liked_by']
