



from flask_restx import fields
from src.comun.utilidades import api


inicio_sesion_doc = api.model('InicioSesionDoc',{
    'correo': fields.String(required=True,example='admin@gmail.com'),
    'contrasenia': fields.String(required=True,example='admin1234'),
})