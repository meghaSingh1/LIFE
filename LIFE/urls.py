from django.contrib import admin
from django.urls import include, path

from socialife.serializers import MyTokenObtainPairView

urlpatterns = [
    path('', include('socialife.urls')),
    path('admin/', admin.site.urls),
    path('api/token/', MyTokenObtainPairView.as_view(), name='my_token_obtain_pair'),

]