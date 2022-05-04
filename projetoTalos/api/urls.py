from django.urls import path
from projetoTalos.api.views import get_todascidades, getcidade, prevdata, sendDataForBi

urlpatterns = [
    path('', get_todascidades),
    path('<str:geocode>/', getcidade),
    path('prever', prevdata),
    path('forbi', sendDataForBi)
]