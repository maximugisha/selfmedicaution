from django.urls import path
from core.tasks import ussd
from core.api import DiseasePredictionAPI

urlpatterns = [
    path('ussd/', ussd, name='ussd'),
    path('predict-disease/', DiseasePredictionAPI.as_view(), name='predict-disease'),
]
