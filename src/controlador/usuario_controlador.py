from flask import request
from flask_restx import Resource
from src.comun.utilidades import db
from sqlalchemy.orm.exc import NoResultFound
from src.comun.utilidades import api
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required 

#importaciones del usuario
from src.modelo.usuario_modelo import UsuarioModelo
from src.esquemas.usuario_esquema import UsuarioEsquema
from src.documentacion.usuario_documentacion import usuario_documentacion
import bcrypt


class UsuarioControlador(Resource):

    @jwt_required()
    @api.expect(usuario_documentacion)
    def post(self):
        try:
            #cargar y validar la informacion del usuario
            usuario = UsuarioEsquema(exclude=['codigo_usuario']).load(request.json)

            #obtiendo la contraseña
            contrasenia = usuario.contrasenia
            #convertila a bytes
            contrasenia_bytes = contrasenia.encode('utf-8')
            #hashearla
            hash = bcrypt.hashpw(contrasenia_bytes,bcrypt.gensalt())

            #actualizar el objeto usuario
            usuario.contrasenia = hash

            #insertar el usuario
            db.session.add(usuario)
            db.session.commit()

            return UsuarioEsquema().dump(usuario), 201
            
        except ValidationError as err:
            print(err)
            mensajes_concatenados = " ".join([f"{clave}: {' '.join(mensajes)}" for clave, mensajes in err.messages_dict.items()])
            return {"mensaje":mensajes_concatenados}, 422
        except Exception as err:
            print(err)
            return {"mensaje":"Algo salió mal, intentalo denuevo."},503 

    @jwt_required()
    @api.expect(usuario_documentacion)
    def put(self):
        try:
            #cargar y validar la informacion del usuario
            usuario = UsuarioEsquema(transient=True).load(request.json)

            #buscar el usuario
            usuario_db = db.session.execute(db.select(UsuarioModelo).where(UsuarioModelo.codigo_usuario == usuario.codigo_usuario)).scalar_one()
            #actualizar la informacion
            usuario_db.nombre = usuario.nombre
            usuario_db.apellido = usuario.apellido
            usuario_db.correo = usuario.correo
            usuario_db.contrasenia = usuario.contrasenia
            #confirmar los cambios
            db.session.commit()

            return UsuarioEsquema().dump(usuario_db), 200
        
        except NoResultFound as err:
            return {"mensaje": "El usuario que intentas actualizar no existe"}, 404
        except ValidationError as err:
            print(err)
            mensajes_concatenados = " ".join([f"{clave}: {' '.join(mensajes)}" for clave, mensajes in err.messages_dict.items()])
            return {"mensaje":mensajes_concatenados}, 422
        except Exception as err:
            print(err)
            return {"mensaje":"Algo salió mal, intentalo denuevo."},503 
    
    @jwt_required()
    def get(self):
        try:
            #consultar todos los usuario
            usuarios = db.session.execute(db.select(UsuarioModelo)).scalars().all()

            return UsuarioEsquema(many=True).dump(usuarios),200

        except Exception as err:
            print(err)
            return {"mensaje":"Algo salió mal, intentalo denuevo."},503 
        

class UsuarioPorCodigoControlador(Resource):

    @jwt_required()
    def get(self, codigo_usuario):
        try:

            usuario = db.session.execute(db.select(UsuarioModelo).where(UsuarioModelo.codigo_usuario == codigo_usuario)).scalar_one()

            return UsuarioEsquema().dump(usuario),200

        except NoResultFound as err:
            return {"mensaje": "El usuario que intentas buscar no existe"}, 404
        except Exception as err:
            print(err)
            return {"mensaje":"Algo salió mal, intentalo denuevo."},503 
        
    @jwt_required()
    def delete(self,codigo_usuario):
        try:

            usuario = db.session.execute(db.select(UsuarioModelo).where(UsuarioModelo.codigo_usuario == codigo_usuario)).scalar_one()

            db.session.delete(usuario)
            db.session.commit()

            return True,204

        except NoResultFound as err:
            return {"mensaje": "El usuario que intentas eliminar no existe"}, 404
        except Exception as err:
            print(err)
            return {"mensaje":"Algo salió mal, intentalo denuevo."},503 