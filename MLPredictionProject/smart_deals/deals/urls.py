from django.urls import path
from . import views

app_name = "deals"

urlpatterns = [
    path("", views.home, name="home"),
    path("predict/", views.predict_coupon, name="predict_coupon"),
]
