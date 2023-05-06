from django.urls import path
from . import views


urlpatterns = [
    path("appointments/create/", views.appointments_create, name="appointments-create"),
    path("appointments/checkout/<int:slot_id>/", views.appointments_checkout, name="appointments-checkout"),
    path("appointments/confirm/<int:slot_id>/", views.appointments_confirm, name="appointments-confirm")
]