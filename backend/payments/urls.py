from django.urls import path
from .views import MakePaymentView

urlpatterns = [
    path("", MakePaymentView.as_view(), name="make-payment"),
]
