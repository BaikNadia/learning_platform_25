from django.urls import path
from . import views

urlpatterns = [
    path('payments/', views.PaymentListAPIView.as_view(), name='payment-list'),
    path('me/', views.UserProfileUpdateView.as_view(), name='user-profile'),
    path('payments/', views.PaymentListAPIView.as_view(), name='payment-list'),
]
