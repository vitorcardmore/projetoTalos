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

