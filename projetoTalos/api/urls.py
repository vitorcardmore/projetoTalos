from django.urls import path
from projetoTalos.api.views import get_todascidades, getcidade, prevdata, sendDataForBi, gethist, gethistcidade

urlpatterns = [
    path('atual/', get_todascidades, name='get_todascidades'),
    path('prever/', prevdata, name='prevdata'),
    path('forbi/', sendDataForBi, name='sendDataForBi'),
    path('atual/<str:geocode>/', getcidade,name='getcidade' ),
    path('historico/',gethist, name='gethist'),
    path('historico/<str:geocode>/', gethistcidade,name='gethistcidade' ),
]