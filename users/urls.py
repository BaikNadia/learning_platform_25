from django.urls import path
from . import views

urlpatterns = [
    path('payments/', views.PaymentListAPIView.as_view(), name='payment-list'),
    path('<int:pk>/', views.UserProfileDetailView.as_view(), name='user-detail'),
    path('me/', views.UserProfileUpdateView.as_view(), name='user-profile'),
    path('register/', views.RegisterUserAPIView.as_view(), name='register'),
]
