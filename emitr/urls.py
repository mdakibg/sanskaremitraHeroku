from django.urls import path
from . import views

app_name = "emitr"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("contact", views.contact_view, name="contact"),
    path("fee/<int:service_id>", views.service_fee_view, name='service_fee'),
]