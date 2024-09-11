from django.urls import path
from core.tasks import ussd

urlpatterns = [
    path('ussd/', ussd, name='ussd'),
]
