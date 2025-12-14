

from flask_restx import fields
from src.comun.utilidades import api


usuario_documentacion = api.model('UsuarioDocumentacion',{
    'codigo_usuario': fields.Integer(required=True,readonly=True),
    'nombre': fields.String(required=True,example='Elzer'),
    'apellido': fields.String(required=True,example='Villela'),
    'correo': fields.String(required=True,example='elzervillela@gmail.com'),
    'contrasenia': fields.String(required=True,example='admin1234'),
    'rol': fields.String(required=True,enum=['Administrador','General'],example='General')
})