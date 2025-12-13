from flask import request
from flask_restx import Resource
from src.documentacion.inicio_sesion_documentacion import inicio_sesion_doc
from src.comun.utilidades import api, db
from flask_jwt_extended import create_access_token
from src.modelo.usuario_modelo import UsuarioModelo
from sqlalchemy.orm.exc import NoResultFound
import bcrypt


class InicioSesionControlador(Resource):

    @api.expect(inicio_sesion_doc)
    def post(self):
        try:
            #obteniendo las credenciales del usuario
            correo = request.json['correo']
            contrasenia = request.json['contrasenia']

            #verificar que exista en la db
            usuario = db.session.execute(
                db.select(UsuarioModelo)
                .where(UsuarioModelo.correo == correo)).scalar_one()
            
            #comparar si la contraseña no es correcta
            if not bcrypt.checkpw(contrasenia.encode("utf-8"),usuario.contrasenia.encode("utf-8")):
                #la contrasena es correcta
                return {"mensaje":"El usuario y/o la contraseñ no son correctos"},401 
                

            #retornanod el token
            access_token = create_access_token(identity=str( usuario.codigo_usuario))
            return access_token, 200
        except NoResultFound as err:
            return {"mensaje":"El usuario y/o la contraseñ no son correctos"},401 
        except Exception as err:
            print(err)
            return {"mensaje":"Algo salió mal, intentalo denuevo."},503 


