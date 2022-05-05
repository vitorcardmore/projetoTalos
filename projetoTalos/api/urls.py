from django.urls import path
from projetoTalos.api.views import get_todascidades, getcidade, prevdata, sendDataForBi, gethist

urlpatterns = [
    path('', get_todascidades, name='get_todascidades'),
    path('<str:geocode>/', getcidade,name='getcidade' ),
    path('prever', prevdata, name='prevdata'),
    path('forbi', sendDataForBi, name='sendDataForBi'),
    path('historico',gethist, name='gethist')
]