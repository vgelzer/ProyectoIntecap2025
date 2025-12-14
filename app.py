
from flask import Flask
from src.comun.utilidades import db, api, ma, jwt
from src.rutas.rutas import RutasGeneral
import os

def crear_aplicacion():
    app = Flask(__name__)



    env = os.getenv('FLASK_ENV', 'desarrollo').lower()
    if env == 'prueba':
        #entorno pruebas
        app.config.from_object("configuracion.ConfiguracionPruebas")
    else:
        #entorno desarrollo o produccion
        app.config.from_object("configuracion.Configuracion")
    

    #iniciar las rutas
    RutasGeneral(api)


    db.init_app(app)
    api.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)


    return app

app = crear_aplicacion()