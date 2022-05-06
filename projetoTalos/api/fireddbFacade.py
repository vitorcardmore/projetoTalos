from projetoTalos.api.models import db
from datetime import datetime
import pytz

tz_sp = pytz.timezone('America/Sao_Paulo')
dia = datetime.now(tz_sp).strftime("%Y%m%d")

def situacao_atual_todas_cidades():
    todosget = db.child('cidades').get().val()
    if todosget:
      resp = []
      try:
        todos = dict(todosget)
      except:
        return None
      else:
        for cidade in todos.values():
          ultimodia = max((cidade['historico'].keys()))
          chaves = list(cidade['historico'][ultimodia].keys())
          chave = max(chaves)
          ultimaat = cidade['historico'][ultimodia][chave]
          cidade['nome'] = cidade['nome'].replace('_',' ')
          del cidade['historico']
          resp.append({'horaultimaAtualizacao':f'{chave}:00', 'DataUltimaAtualizacao':ultimodia, **ultimaat, **cidade})
        return resp

def situacao_atual_cidade(geocode):
    cidade = dict(db.child('cidades').child(geocode).get().val())
    if cidade:
      try:
          ultimodia = max(tuple(cidade['historico'].keys()))
      except:
          return None
      else:
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
        resp.append({'horaultimaAtualizacao':f'{horaatual}:00', 'DataUltimaAtualizacao':str(date).replace('-','/') ,'variacao':round(ultimaat['temperatura']-anterior['temperatura'],2), **ultimaat, **cidade})
      return resp


def get_historico_todas_cidades():
  todosget = db.child('cidades').get().val()
  if todosget:
    try:
      todos = dict(todosget)
    except:
      return None
    else:
      return todos
