from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from system_user.views import MyTokenObtainPairView
from django.conf.urls.static import static
from chat_project import settings




urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('system_user.urls')),
    path('api/', include('complaint.urls')),


    path('', include('chat.routing')),
    path('ht/', include('http_app.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
