
from flask import request
from flask_restx import Resource
from src.comun.utilidades import db
from sqlalchemy.orm.exc import NoResultFound
from src.comun.utilidades import api
from marshmallow import ValidationError

from src.modelo.pokemon_x_tipo_modelo import PokemonXTipoModelo
from src.esquemas.pokemon_x_tipo_esquema import PokemonXTipoEsquema
from src.documentacion.pokemon_x_tipo_documentacion import pokemon_x_tipo_documentacion
from flask_jwt_extended import jwt_required
from src.documentacion.error_documentacion import error_documentacion


class PokemonXTipoControlador(Resource):


    
    @api.doc(description="Permite asignar un tipo a un pokemon")
    @api.expect(pokemon_x_tipo_documentacion)
    @api.response(503,'Error en la consulta del servidor, consulte logs',error_documentacion)
    @api.response(422,'Entidad improcesable',error_documentacion)
    @api.response(403,'No cuenta con los permisos necesarios para realizar esta accion')
    @api.response(401,'No tiene autorizacion')
    @api.response(200,'Actualizacion exitosa', pokemon_x_tipo_documentacion)
    @jwt_required()
    def post(self):
        try:
            #obtener tipo json
            pokemon_tipo_json = request.json

            #validar reglas
            pokemonXTipoEsquema = PokemonXTipoEsquema(transient=True)
            pokemon_x_tipo_validado = pokemonXTipoEsquema.load(pokemon_tipo_json)
            
            db.session.add(pokemon_x_tipo_validado)
            db.session.commit()


            return PokemonXTipoEsquema().dump(pokemon_x_tipo_validado),200
        except ValidationError as err:
            print(err)
            mensajes_concatenados = " ".join([f"{clave}: {' '.join(mensajes)}" for clave, mensajes in err.messages_dict.items()])
            return {"mensaje":mensajes_concatenados}, 422
        except Exception as err:
            print(err)
            return {"mensaje":"Algo salió mal, intentalo denuevo."},503 
        

class PokemonXTipoPorCodigosControlador(Resource):

    @api.doc(description="Permite eliminar un tipo a un pokemon")
    @api.response(503,'Error en la consulta del servidor, consulte logs',error_documentacion)
    @api.response(422,'Entidad improcesable',error_documentacion)
    @api.response(403,'No cuenta con los permisos necesarios para realizar esta accion')
    @api.response(401,'No tiene autorizacion')
    @api.response(204,'Eliminacion exitosa')
    @jwt_required()
    def delete(self,codigo_pokemon:int, codigo_tipo:int):
        try:
            #buscar el elemento a ver si existe
            #select * from pokemon_x_tipo where codigo_tipo = ? and codigo_pokemon=?
            pokemon_db = db.session.execute(db.select(PokemonXTipoModelo)
                                            .where(PokemonXTipoModelo.codigo_pokemon == codigo_pokemon)
                                            .where(PokemonXTipoModelo.codigo_tipo == codigo_tipo)
                                            ).scalar_one()

            #elimianr el recurso
            db.session.delete(pokemon_db)
            #confirmar
            db.session.commit()

            return True,204


        except NoResultFound as err:
            print(err)
            return {"mensaje":"No existe el tipo asignado al pokemon que quieres eliminar"},404

        except Exception as err:
            print(err)
            #excepcion general
            return {"mensaje":"Algo salió mal, intentalo denuevo."},503 

