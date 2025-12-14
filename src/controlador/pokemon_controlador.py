from flask import request
from flask_restx import Resource
from src.comun.utilidades import db
from sqlalchemy.orm.exc import NoResultFound
from src.comun.utilidades import api
from marshmallow import ValidationError
from src.documentacion.pokemon_documentacion import pokemon_documentacion
from src.esquemas.pokemon_esquema import PokemonEsquema
from src.modelo.pokemon_modelo import PokemonModelo
from flask_jwt_extended import jwt_required 
from src.documentacion.error_documentacion import error_documentacion


#eliminacion y busqueda por tipo por su codigo tipo
class PokemonControladorPorCodigoPokemon(Resource):

    #select * from table condicion
    @api.doc(description="Permite actualizar un pokemon")
    @api.response(503,'Error en la consulta del servidor, consulte logs',error_documentacion)
    @api.response(404,'No existe el tipo que se quiere actualizar en la db',error_documentacion)
    @api.response(403,'No cuenta con los permisos necesarios para realizar esta accion')
    @api.response(401,'No tiene autorizacion')
    @api.response(200,'Consulta exitosa', pokemon_documentacion)
    @jwt_required()
    def get(self, codigo_pokemon:int):
        try:
            #buscar el elemento a ver si existe
            pokemon_db = db.session.execute(db.select(PokemonModelo).where(PokemonModelo.codigo_pokemon == codigo_pokemon)).scalar_one()

            #objeto de esquema
            pokemon_esquema = PokemonEsquema()

            return pokemon_esquema.dump(pokemon_db),200

        except NoResultFound as err:
            print(err)
            return {"mensaje":"No existe el pokemon que quiere consultar"},404

        except Exception as err:
            print(err)
            #excepcion general
            return {"mensaje":"Algo salió mal, intentalo denuevo."},503 
            


    #delete from tabla condicion
    @api.doc(description="Permite actualizar un pokemon")
    @api.response(503,'Error en la consulta del servidor, consulte logs',error_documentacion)
    @api.response(404,'No existe el tipo que se quiere actualizar en la db',error_documentacion)
    @api.response(403,'No cuenta con los permisos necesarios para realizar esta accion')
    @api.response(401,'No tiene autorizacion')
    @api.response(204,'Eliminacion exitosa')
    @jwt_required()
    def delete(self, codigo_pokemon:int):
        try:
            #buscar el elemento a ver si existe
            pokemon_db = db.session.execute(db.select(PokemonModelo).where(PokemonModelo.codigo_pokemon == codigo_pokemon)).scalar_one()

            #elimianr el recurso
            db.session.delete(pokemon_db)
            #confirmar
            db.session.commit()

            return True,204


        except NoResultFound as err:
            print(err)
            return {"mensaje":"No existe el pokemon que quieres eliminar"},404

        except Exception as err:
            print(err)
            #excepcion general
            return {"mensaje":"Algo salió mal, intentalo denuevo."},503 
            

class PokemonControlador(Resource):

    #Read
    @api.doc(description="Permite obtener una lista de pokemons")
    @api.response(503,'Error en la consulta del servidor, consulte logs',error_documentacion)
    @api.response(404,'No existe el tipo que se quiere actualizar en la db',error_documentacion)
    @api.response(403,'No cuenta con los permisos necesarios para realizar esta accion')
    @api.response(401,'No tiene autorizacion')
    @api.response(200,'Consulta exitosa', [pokemon_documentacion])
    @jwt_required()
    def get(self):
        try:
            #select * from tipo
            pokemon = db.session.execute(
                db.select(PokemonModelo)
                                    ).scalars().all()

            lista_json = PokemonEsquema(many=True).dump(pokemon)

            return lista_json,200
            
        except Exception as err:
            return {"mensaje":"Algo salió mal, intentalo denuevo."},503 
        
    
    #Create
    
    @api.doc(description="Permite crear un pokemon")
    @api.expect(pokemon_documentacion)
    @api.response(503,'Error en la consulta del servidor, consulte logs',error_documentacion)
    @api.response(422,'Entidad improcesable',error_documentacion)
    @api.response(403,'No cuenta con los permisos necesarios para realizar esta accion')
    @api.response(401,'No tiene autorizacion')
    @api.response(200,'Creacion exitosa', pokemon_documentacion)
    @jwt_required()
    def post(self):
        try:
            #obtener tipo json
            pokemon_json = request.json

            #validar reglas
            pokemon_esquema = PokemonEsquema(exclude=['codigo_pokemon'])
            pokemon_validado = pokemon_esquema.load(pokemon_json)
            
            db.session.add(pokemon_validado)
            db.session.commit()


            return PokemonEsquema().dump(pokemon_validado),200
        except ValidationError as err:
            print(err)
            mensajes_concatenados = " ".join([f"{clave}: {' '.join(mensajes)}" for clave, mensajes in err.messages_dict.items()])
            return {"mensaje":mensajes_concatenados}, 422
        except Exception as err:
            print(err)
            return {"mensaje":"Algo salió mal, intentalo denuevo."},503 
        
    
    #Update
    @api.doc(description="Permite actualizar un tipo")
    @api.expect(pokemon_documentacion)
    @api.response(503,'Error en la consulta del servidor, consulte logs',error_documentacion)
    @api.response(404,'No existe el pokemon que se quiere actualizar en la db',error_documentacion)
    @api.response(422,'Entidad improcesable',error_documentacion)
    @api.response(403,'No cuenta con los permisos necesarios para realizar esta accion')
    @api.response(401,'No tiene autorizacion')
    @api.response(200,'Actualizacion exitosa', pokemon_documentacion)
    @jwt_required()
    def put(self):
        #objeto y lo validar
        #select * from Pokemon where = 1
        try:

            #validando la entrada
            pokemon = PokemonEsquema().load(request.json)

            #actualizando el campo
            pokemon_db = db.session.execute(db.select(PokemonModelo).where(PokemonModelo.codigo_pokemon == pokemon.codigo_pokemon)).scalar_one()
            pokemon_db.nombre = pokemon.nombre
            pokemon_db.nivel = pokemon.nivel
            pokemon_db.descripcion = pokemon.descripcion
            db.session.commit()

            return PokemonEsquema().dump(pokemon_db),200
        except ValidationError as err:
            print(err)
            mensajes_concatenados = " ".join([f"{clave}: {' '.join(mensajes)}" for clave, mensajes in err.messages_dict.items()])
            return {"mensaje":mensajes_concatenados}, 422
        except NoResultFound as err:
            print(err)
            return {"mensaje":"No existe el pokemon que intentas actualizar"},404
        except Exception as err:
            return {"mensaje":"Algo salió mal, intentalo denuevo."},503 
        
