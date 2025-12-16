from django.urls import path
from interns_challenges_number1.main import PayoutListAPIView

urlpatterns = [
    path("payout/", PayoutListAPIView.as_view(), name="payout-list"),
]