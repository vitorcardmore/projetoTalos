from django.urls import path
from projetoTalos.api.views import get_todascidades, getcidade, prevdata

urlpatterns = [
    path('', get_todascidades),
    path('<str:geocode>/', getcidade),
    path('prever', prevdata)
]