from django.urls import path
from projetoTalos.api.views import get_todascidades, getcidade

urlpatterns = [
    path('', get_todascidades),
    path('<str:geocode>/', getcidade)
]