from django.urls import path
from . import views

urlpatterns = [
    path('', views.LessonListCreateAPIView.as_view(), name='lesson-list-create'),
    path('<int:pk>/', views.LessonRetrieveUpdateDestroyAPIView.as_view(), name='lesson-retrieve-update-destroy'),
    path('toggle-subscribe/', views.SubscriptionToggleAPIView.as_view(), name='toggle-subscribe'),
]
