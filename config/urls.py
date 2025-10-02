from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


from materials import views
from materials.views import CourseViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'courses', CourseViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="Your API description",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),

    # API маршруты от роутера
    path('api/', include(router.urls)),

    # API
    path('api/', include('materials.urls')),           # уроки
    path('api/courses/', include('materials.urls')),  # курсы + подписка
    path('api/users/', include('users.urls')),

    # Уроки
    path('api/lessons/', include('materials.urls')),

    # Подписка
    path('api/course-subscribe/', views.SubscriptionToggleAPIView.as_view(), name='course-subscribe'),

    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
