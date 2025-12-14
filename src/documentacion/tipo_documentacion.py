

from flask_restx import fields
from src.comun.utilidades import api


tipo_documentacion = api.model('TipoDocumentacionEntrada',{
    'codigo_tipo': fields.Integer(required=True,readonly=True),
    'nombre': fields.String(required=True,example='Agua')
})