from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from materials.views import CourseViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/lessons/', include('materials.urls')),
    path('api/users/', include('users.urls')),
]
