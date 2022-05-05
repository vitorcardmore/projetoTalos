from django.urls import path
from projetoTalos.web.views import landingpage, bipage, manualApi

urlpatterns = [
    path('',landingpage, name='landingpage'),
    path('situacao-atual', bipage, name='bipage'),
    path('manual-api', manualApi, name='manualApi')
]