from projetoTalos.api.models import db
from datetime import datetime
import pytz

tz_sp = pytz.timezone('America/Sao_Paulo')
dia = datetime.now(tz_sp).strftime("%Y%m%d")

def situacao_atual_todas_cidades():
    todosget = db.child('cidades').get().val()
    todos = dict(todosget)
    resp = []
    for cidade in todos.values():
      chaves = tuple(cidade['historico'][dia].keys())
      chave = max(chaves)
      atual = cidade['historico'][dia][chave]
      resp.append({cidade["nome"]:{'ultimaAtualizacao':f'{chave}:00','situacao':atual}})
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
          chaves = list(cidade['historico'][dia].keys())
          chave = max(chaves)
          chaves.remove(chave)
          chaveaterior = max(chaves)
          atual = cidade['historico'][dia][chave]
          anterior = cidade['historico'][dia][chaveaterior]
          atual['nome'] = atual['nome'].replace('_',' ')
          del cidade['historico']
          resp.append({'horaultimaAtualizacao':f'{chave}:00', 'DataUltimaAtualizacao':dia ,'variacao':round(atual['temperatura']-anterior['temperatura'],2), **atual, **cidade})
        return resp 