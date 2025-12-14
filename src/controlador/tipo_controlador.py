from flask import request
from flask_restx import Resource
from src.comun.utilidades import db
from src.modelo.tipo_modelo import TipoModelo
from sqlalchemy.orm.exc import NoResultFound
from src.esquemas.tipo_esquema import TipoEsquema
from src.comun.utilidades import api
from src.documentacion.tipo_documentacion import tipo_documentacion
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required
from src.documentacion.error_documentacion import error_documentacion


#eliminacion y busqueda por tipo por su codigo tipo
class TipoControladorPorCodigoTipo(Resource):

    #select * from table condicion
    @api.doc(description="Permite consultar la informacion de un tipos por su codigo tipo")
    @api.response(503,'Error en la consulta del servidor, consulte logs',error_documentacion)
    @api.response(404,'No se encontro el recurso en la base de datos',error_documentacion)
    @api.response(403,'No cuenta con los permisos necesarios para realizar esta accion')
    @api.response(401,'No tiene autorizacion')
    @api.response(200,'Consulta exitosa',tipo_documentacion)
    @jwt_required()
    def get(self, codigo_tipo:int):
        try:
            #buscar el elemento a ver si existe
            tipo_db = db.session.execute(db.select(TipoModelo).where(TipoModelo.codigo_tipo == codigo_tipo)).scalar_one()

            #objeto de esquema
            tipo_esquema = TipoEsquema()

            return tipo_esquema.dump(tipo_db),200

        except NoResultFound as err:
            print(err)
            return {"mensaje":"No existe el tipo que quiere consultar"},404

        except Exception as err:
            print(err)
            #excepcion general
            return {"mensaje":"Algo salió mal, intentalo denuevo."},503 
            


    #delete from tabla condicion
    @api.doc(description="Permite eliminar la informacion de un tipos por su codigo tipo")
    @api.response(503,'Error en la consulta del servidor, consulte logs',error_documentacion)
    @api.response(404,'No se encontro el recurso que se quiere eliminar en la base de datos',error_documentacion)
    @api.response(403,'No cuenta con los permisos necesarios para realizar esta accion')
    @api.response(401,'No tiene autorizacion')
    @api.response(204,'Eliminación exitosa')
    @jwt_required()
    def delete(self, codigo_tipo:int):
        try:
            #buscar el elemento a ver si existe
            tipo_db = db.session.execute(db.select(TipoModelo).where(TipoModelo.codigo_tipo == codigo_tipo)).scalar_one()

            #elimianr el recurso
            db.session.delete(tipo_db)
            #confirmar
            db.session.commit()

            return True,204


        except NoResultFound as err:
            print(err)
            return {"mensaje":"No existe el tipo que quieres eliminar"},404

        except Exception as err:
            print(err)
            #excepcion general
            return {"mensaje":"Algo salió mal, intentalo denuevo."},503 
            

class TipoControlador(Resource):

    #Read
    @api.doc(description="Permite obtener una lista de tipos")
    @api.response(503,'Error en la consulta del servidor, consulte logs',error_documentacion)
    @api.response(403,'No cuenta con los permisos necesarios para realizar esta accion')
    @api.response(401,'No tiene autorizacion')
    @api.response(200,'Consulta exitosa', [tipo_documentacion])
    @jwt_required()
    def get(self):
        try:
            #select * from tipo
            tipos = db.session.execute(
                db.select(TipoModelo)
                                    ).scalars().all()

            lista_json = TipoEsquema(many=True).dump(tipos)

            return lista_json,200
            
        except Exception as err:
            return {"mensaje":"Algo salió mal, intentalo denuevo."},503 
        
    
    #Create
    @api.doc(description="Permite crear un tipo")
    @api.expect(tipo_documentacion)
    @api.response(503,'Error en la consulta del servidor, consulte logs',error_documentacion)
    @api.response(422,'Entidad improcesable',error_documentacion)
    @api.response(403,'No cuenta con los permisos necesarios para realizar esta accion')
    @api.response(401,'No tiene autorizacion')
    @api.response(200,'Creacion exitosa', tipo_documentacion)
    @jwt_required()
    def post(self):
        try:
            #obtener tipo json
            tipo_json = request.json

            #validar reglas
            tipo_esquema = TipoEsquema(exclude=['codigo_tipo'])
            tipo_validado = tipo_esquema.load(tipo_json)
            
            db.session.add(tipo_validado)
            db.session.commit()

            #objeto de esquema
            tipo_esquema = TipoEsquema()

            return tipo_esquema.dump(tipo_validado),200
        except ValidationError as err:
            print(err)
            mensajes_concatenados = " ".join([f"{clave}: {' '.join(mensajes)}" for clave, mensajes in err.messages_dict.items()])
            return {"mensaje":mensajes_concatenados}, 422
        except Exception as err:
            print(err)
            return {"mensaje":"Algo salió mal, intentalo denuevo."},503 
        
    
    #Update
    @api.doc(description="Permite actualizar un tipo")
    @api.expect(tipo_documentacion)
    @api.response(503,'Error en la consulta del servidor, consulte logs',error_documentacion)
    @api.response(404,'No existe el tipo que se quiere actualizar en la db',error_documentacion)
    @api.response(422,'Entidad improcesable',error_documentacion)
    @api.response(403,'No cuenta con los permisos necesarios para realizar esta accion')
    @api.response(401,'No tiene autorizacion')
    @api.response(200,'Actualizacion exitosa', tipo_documentacion)
    @jwt_required()
    def put(self):
        #objeto y lo validar
        #select * from TipoModelo where = 1
        try:
            #obtener tipo json
            tipo_json = request.json

            #validando la entrada
            tipo = TipoEsquema().load(tipo_json)

            #actualizando el campo
            tipo_db = db.session.execute(db.select(TipoModelo).where(TipoModelo.codigo_tipo == tipo.codigo_tipo)).scalar_one()
            tipo_db.nombre = tipo.nombre
            db.session.commit()

            return TipoEsquema().dump(tipo_db),200
        except ValidationError as err:
            print(err)
            mensajes_concatenados = " ".join([f"{clave}: {' '.join(mensajes)}" for clave, mensajes in err.messages_dict.items()])
            return {"mensaje":mensajes_concatenados}, 422
        except NoResultFound as err:
            print(err)
            return {"mensaje":"No existe el tipo que intentas actualizar"},404
        except Exception as err:
            return {"mensaje":"Algo salió mal, intentalo denuevo."},503 
        
