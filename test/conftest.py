
import pytest
import os
from app import crear_aplicacion
from src.comun.utilidades import db
from src.modelo.tipo_modelo import TipoModelo
from flask_jwt_extended import create_access_token


@pytest.fixture(scope='session')
def app():
    os.environ['FLASK_ENV'] = 'prueba'

    app = crear_aplicacion()

    with app.app_context():
        #eliminar la db
        db.drop_all()
        db.create_all()
    
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture(scope='session')
def token_cliente_admin(app):
    #usuario 1 admin
    token = ''
    with app.app_context():
        token = create_access_token(
            identity="1",
            additional_claims={"rol":"Administrador"}
            )
    
    return token

@pytest.fixture()
def cliente(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def datos(app):

    with app.app_context():
        #crear data de tipos
        t1 = TipoModelo(
            nombre = "Fuego"
        )
        t2 = TipoModelo(
            nombre = "Planta"
        )
        t3 = TipoModelo(
            nombre = "Electrico"
        )

        db.session.add_all([t1,t2,t3])
        db.session.commit()
    yield
    with app.app_context():
        db.session.query(TipoModelo).delete()
        db.session.commit()