from projetoTalos.api.models import db
from datetime import datetime, timedelta
import pytz

tz_sp = pytz.timezone('America/Sao_Paulo')
dia = datetime.now(tz_sp).strftime("%Y%m%d")

def situacao_atual_todas_cidades(uf, ddd):
    if ddd:
      todosget = db.child("cidades").order_by_child("ddd").equal_to(int(ddd)).get().val()
    elif uf:
      todosget = db.child("cidades").order_by_child("uf").equal_to(uf).get().val()
    else:
      todosget = db.child('cidades').get().val()

    if todosget:
      resp = {}
      try:
        todos = dict(todosget)
      except:
        return None
      else:
        for cod, cidade in todos.items():
          ultimodia = max((cidade['historico'].keys()))
          chaves = list(cidade['historico'][ultimodia].keys())
          chave = max(chaves)
          ultimaat = cidade['historico'][ultimodia][chave]
          cidade['nome'] = cidade['nome'].replace('_',' ')
          del cidade['historico']
          resp[cod] = {'horaultimaAtualizacao':f'{chave}:00', 'DataUltimaAtualizacao':ultimodia, **ultimaat, **cidade}
        return resp

def situacao_atual_cidade(geocode):
    cidade = db.child('cidades').child(geocode).get().val()
    if cidade:
      try:
          cidade = dict(cidade)
      except:
          return None
      else:
          ultimodia = max(tuple(cidade['historico'].keys()))
          chave = max(tuple(cidade['historico'][ultimodia].keys()))
          atual = cidade['historico'][ultimodia][chave]
          return {cidade["nome"]:{'ultimaAtualizacao':{'dia':ultimodia, 'hora':f'{chave}:00'},'situacao':atual}}

def situacaodeplotagembi():
  todosget = db.child('cidades').get().val()
  if todosget:
    resp = []
    try:
      todos = dict(todosget)
    except:
      return None
    else:
      for cidade in todos.values():

        historico = list(cidade['historico'].keys())
        diaatual = historico.pop()

        horas = list(cidade['historico'][diaatual].keys())
        horaatual = horas.pop()
        
        if horas:
          diaanterior = diaatual
          horaanterior = horas.pop()
        else:
          diaanterior = historico.pop()
          horaanterior = list(cidade['historico'][diaanterior].keys()).pop()
        
        ultimaat = cidade['historico'][diaatual][horaatual]
        anterior = cidade['historico'][diaanterior][horaanterior]
        cidade['nome'] = cidade['nome'].replace('_',' ')
        del cidade['historico']
        date = datetime.strptime(diaatual, "%Y%m%d").date()

        resp.append({'horaultimaAtualizacao':f'{horaatual}:00', 
        'DataUltimaAtualizacao':str(date).replace('-','/') ,
        'variacao':round(ultimaat['temperatura']-anterior['temperatura'],2), 
        **ultimaat, **cidade})

      return resp

def datarange(val, defa):
      if val == None: 
        return defa
      else: 
        return val

def dataper(ini, fim):
  date = datetime.strptime(ini, "%Y%m%d")
  datafim = datetime.strptime(fim, "%Y%m%d")
  while date <= datafim:
    yield datetime.strftime(date, "%Y%m%d")
    date = date + timedelta(days=1)

def get_historico_todas_cidades(uf,ddd, ini, fim):

  if ddd:
    todosget = db.child("cidades").order_by_child("ddd").equal_to(int(ddd)).get().val()
  elif uf:
    todosget = db.child("cidades").order_by_child("uf").equal_to(uf).get().val()
  else:
    todosget = db.child('cidades').get().val()

  if todosget:
    try:
      todos = dict(todosget)
    except:
      return None
    else:
      if ini != None or fim != None:
        ini = datarange(ini,'20220501')
        tz_sp = pytz.timezone('America/Sao_Paulo')
        dia = datetime.now(tz_sp).strftime("%Y%m%d")
        fim = datarange(fim,dia)  
        for j in todos.keys():
          t = dict()
          for i in dataper(ini, fim):
            try:  
              t[i] = todos[j]['historico'][i]
            except KeyError:
              continue
          todos[j]['historico'] = t
      return todos

def get_historico_cidade(ini, fim, geocode):
    histcidade =  db.child('cidades').child(geocode).get().val()
    
    if ini != None or fim != None:
      ini = datarange(ini,'0')
      tz_sp = pytz.timezone('America/Sao_Paulo')
      dia = datetime.now(tz_sp).strftime("%Y%m%d")
      fim = datarange(fim,dia)
      histcidade['historico'] = db.child('cidades').child(geocode).child('historico').order_by_key().start_at(ini).end_at(fim).get().val()

    return histcidade
