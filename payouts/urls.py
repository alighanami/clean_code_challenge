from django.urls import path
from .views import PayoutListAPIView

urlpatterns = [
    path("payouts/", PayoutListAPIView.as_view()),
]
