

from flask_restx import fields
from src.comun.utilidades import api


error_documentacion = api.model('ErrorDocumentacion',{
    'mensaje': fields.String(required=True,example='Error de la consulta')
})