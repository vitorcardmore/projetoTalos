from django.shortcuts import render
import projetoTalos.api.fireddbFacade as facade
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import json
import pickle
import sklearn
from sklearn.preprocessing import StandardScaler
from projetoTalos.settings import BASE_DIR, ACESSPREV
import numpy
from datetime import datetime
import pytz
import asyncio
import aiohttp
import requests


@api_view(['GET'])
def get_todascidades(request):
    resp = facade.situacao_atual_todas_cidades()
    return Response(resp, status=status.HTTP_200_OK)

@api_view(['GET'])
def getcidade(request, geocode):
    resp = facade.situacao_atual_cidade(geocode)
    return Response(resp, status=status.HTTP_200_OK)


@api_view(['POST',])
def prevdata(request):
    reqdata = request.data

    if reqdata['acessprev'] == ACESSPREV:

        # cpnfiguração de data e hora
        tz_sp = pytz.timezone('America/Sao_Paulo')
        dia = datetime.now(tz_sp).strftime("%Y%m%d")
        hora = datetime.now(tz_sp).strftime("%H")
        chaves = ['JL09-YshZ72ImHrqqo-ZtgjnFHliQR-P5PsBHJ3Sepc','3jPJR_BwjQwsEmB88XLZxMJBJVSC-slHGS3B_G5uiao']

        #dados das cidades 
        with open(f'{BASE_DIR}/projetoTalos/api/rede/cidades.json', encoding='utf8') as f:
            cidadescord = json.loads(f.read())

        #configuração da rede neural
        rede_neural = pickle.load(open(f'{BASE_DIR}/projetoTalos/api/rede/rede_neural.sav', 'rb'))
        scaler =  StandardScaler()
        prever = []
        dados = {}
        ordemcidade = []

        loop = asyncio.new_event_loop()
        loop.run_until_complete(main(cidadescord, prever, dados, ordemcidade, chaves))

        s = scaler.fit_transform(prever)
        previsoes = rede_neural.predict(s)

        data = {}
        for i, cidade in enumerate(ordemcidade):
            dados[cidade]["rf"] = int(previsoes[i])
            data[f'cidades/{cidade}/historico/{dia}/{hora}'] = dados[cidade]

        path  = 'https://talos-38497-default-rtdb.firebaseio.com/.json'
        headers = {'content-type': 'application/json; charset=UTF-8'}

        r = requests.patch(path, headers=headers, data=json.dumps(data, **{}).encode("utf-8"))
        if r.status_code == 200:
            return Response({'status':'200','desc':'sucesso', 'dados atualizados':r.text}, status=status.HTTP_200_OK)
        else:
            return Response({'status':'400','desc':'bad request'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'status':'403','desc':'acesso negado'}, status=status.HTTP_403_FORBIDDEN)   
async def req(session, url, cidade, prever, dados, ordemcidade):
    async with session.get(url) as resp:
        resposta = await resp.json()

        try:
            resposta = resposta['results'][0]

        except:
          pass

        else:
            temperatura = resposta['temperature']['value']
            umidade = resposta['relativeHumidity']
            ventovelo = resposta['wind']['speed']['value'] / 3.6
            ventodir = resposta['wind']['direction']['localizedDescription']
            uv = resposta['uvIndex']
            pressao = resposta['pressure']['value']
            preciptacao = resposta['precipitationSummary']['pastHour']['value']
            tempar = resposta["windChillTemperature"]['value']
            condicao = resposta['phrase']
            coberturadenuvens = resposta['cloudCover']

            lista = [preciptacao, tempar, umidade, ventovelo]

            dados[cidade] = {
                    'temperatura': temperatura, 
                    'umidadeRelativaDoAr':umidade,
                    'velocidadeDoVento':round(ventovelo,3),
                    'temperaturaDoAr':tempar,
                    'indiceUv':uv, 
                    'pressao': pressao ,
                    'precipitacao':preciptacao,
                    'condicao':condicao, 
                    'coberturaDeNuvens':coberturadenuvens
                }

            prever.append(lista)
            ordemcidade.append(cidade)

async def main(cidadescord, prever, dados, ordemcidade, chaves):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i,t in enumerate(cidadescord.items()):
            cidade, cordenada = t
            chave = chaves[int(i%2 == 0)]
            scordd = f'{cordenada["latitude"]},{cordenada["longitude"]}'
            url = f'https://atlas.microsoft.com/weather/currentConditions/json?api-version=1.0&query={scordd}&subscription-key={chave}&language=pt-br'
            tasks.append(asyncio.ensure_future(req(session, url, cidade, prever, dados, ordemcidade)))      
        await asyncio.gather(*tasks)

@api_view(['GET',])
def sendDataForBi(request):
    resp = facade.situacaodeplotagembi()
    if resp:
        return Response(resp, status=status.HTTP_200_OK)
    else:
        return Response({'status':'400','desc':'bad request'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET',])
def gethist(request):
    resp = facade.get_historico_todas_cidades()
    if resp:
        return Response(resp, status=status.HTTP_200_OK)
    else:
        return Response({'status':'400','desc':'bad request'}, status=status.HTTP_400_BAD_REQUEST)