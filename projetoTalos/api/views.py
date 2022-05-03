from django.shortcuts import render
import projetoTalos.api.fireddbFacade as facade
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['GET'])
def get_todascidades(request):
    resp = facade.situacao_atual_todas_cidades()
    return Response(resp, status=status.HTTP_200_OK)

@api_view(['GET'])
def getcidade(request, geocode):
    resp = facade.situacao_atual_cidade(geocode)
    return Response(resp, status=status.HTTP_200_OK)

@api_view(['POST'])
def prevdata(request):
    data = request.data
    auth = request.GET.get('auth')
    if auth:
        return Response({'status:200','bbbb':data}, status=status.HTTP_200_OK)
    else:
        return Response({'ala':'deumerda'})