from django.urls import path
from . import views

urlpatterns = [
    # Уроки
    path('', views.LessonListCreateAPIView.as_view(), name='lesson-list-create'),
    path('<int:pk>/', views.LessonRetrieveUpdateDestroyAPIView.as_view(), name='lesson-retrieve-update-destroy'),

    # Курсы (ViewSet требует router)
]
