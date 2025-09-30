from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from materials import views
from materials.views import CourseViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    # API маршруты от роутера
    path('api/', include(router.urls)),

    # Уроки
    path('api/lessons/', include('materials.urls')),

    # Подписка
    path('api/course-subscribe/', views.SubscriptionToggleAPIView.as_view(), name='course-subscribe'),

    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
