from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
import notifications
from users.views import RegisterView, CustomTokenObtainPairView
from habits.views import HabitViewSet, PublicHabitListViewSet
from notifications.views import TelegramWebhookView

router = DefaultRouter()
router.register(r'habits', HabitViewSet, basename='habit')
router.register(r'public-habits', PublicHabitListViewSet, basename='public-habit')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/', include(router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/telegram/webhook/', notifications.views.TelegramWebhookView.as_view(), name='telegram_webhook'),
]