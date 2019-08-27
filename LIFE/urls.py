from django.contrib import admin
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static

from socialife.serializers import MyTokenObtainPairView


urlpatterns = [
    path('', include('socialife.urls')),
    path('admin/', admin.site.urls),
    path('api/token/', MyTokenObtainPairView.as_view(), name='my_token_obtain_pair'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)