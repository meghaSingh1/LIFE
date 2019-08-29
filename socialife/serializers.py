from .models import MyUser, Post, Comment, Notification, ChatRoom, Message, PostImage
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

# class FollowerField(serializers.Field):
#     def get_attribute(self, instance):
#         # We pass the object instance onto `to_representation`,
#         # not just the field attribute.
#         return instance

#     def to_representation(self, value):
#         followers = MyUser.objects.filter(instance__in = followings)
#         return value.__class__.__name__

class UserSerializer(serializers.ModelSerializer):
    followers = serializers.StringRelatedField(many = True)
    
    class Meta:
        model = MyUser
        fields = ['email', 'first_name', 'last_name', 'profile_name', 'get_followings', 'followers', 'avatar']

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    date_created = serializers.DateTimeField('%B %d %Y at %H:%M')
    class Meta:
        model = Comment
        fields = ['user', 'content', 'date_created',]

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['image']

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    liked_by = UserSerializer(many = True)
    date_created = serializers.DateTimeField('%B %d %Y at %H:%M')
    comments = CommentSerializer(many = True)
    images = PostImageSerializer(many = True)
    class Meta:
        model = Post
        fields = ['uuid', 'user', 'text_content', 'date_created', 'liked_by', 'comments', 'images']

class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    from_user = UserSerializer()
    class Meta:
        model = Notification
        fields = ['user', 'from_user', 'content', 'is_read', 'url']

class ChatRoomSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)
    notice_by_users = UserSerializer(many=True)
    class Meta:
        model = ChatRoom
        fields = ['users', 'uuid', 'is_group_chat', 'notice_by_users', 'last_interaction']

class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    read_by_users = UserSerializer(many = True)
    chat_room = ChatRoomSerializer()
    class Meta:
        model = Message
        fields = ['user', 'read_by_users', 'chat_room', 'date_created', 'content']