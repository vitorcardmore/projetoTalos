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
    chaves = tuple(cidade['historico'][dia].keys())
    chave = min(chaves)
    atual = cidade['historico'][dia][chave]
    return {cidade["nome"]:{'ultimaAtualizacao':f'{chave}:00','situacao':atual}}

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
        ultimodia = max((cidade['historico'].keys()))
        chaves = list(cidade['historico'][ultimodia].keys())
        chave = max(chaves)
        chaves.remove(chave)
        chaveaterior = max(chaves)
        ultimaat = cidade['historico'][ultimodia][chave]
        anterior = cidade['historico'][ultimodia][chaveaterior]
        cidade['nome'] = cidade['nome'].replace('_',' ')
        del cidade['historico']
        date = datetime.strptime(ultimodia, "%Y%m%d").date()
        resp.append({'horaultimaAtualizacao':f'{chave}:00', 'DataUltimaAtualizacao':str(date).replace('-','/') ,'variacao':round(ultimaat['temperatura']-anterior['temperatura'],2), **ultimaat, **cidade})
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
