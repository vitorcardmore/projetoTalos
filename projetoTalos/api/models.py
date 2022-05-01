import string
import pyrebase
from projetoTalos.settings import firebaseConfig

firebase  = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
