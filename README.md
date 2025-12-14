# Api Pokemon

Esta api contempla el manejo de la informacion para pokemons y sus tipos

## Índice

- [Instalación](#instalación)
- [Uso](#uso)
- [Pruebas](#pruebas)
- [Docker](#docker)
- [Documentacion](#documentación)

## Instalación

1. Clona el repositorio
2. Crea tu archivo .env para manejar los entorno adecuados
3. En tu archivo .env debe almacenar las siguientes variables de entorno

```
JWT_SECRET_KEY="tu llave secreta"

SQLALCHEMY_DATABASE_URI = 'url a la base de pruebas'
```

## Uso

Se corre de forma local para produccion o entornos de desarrollo.

### Configuración de entorno

Se programo este microservicio en python 3.12

Crea un entorno virtual

```
python-3 -m venv .venv
```

Activar el entorno virtual de python linux

```
source .venv/bin/activate
```

Instalar dependencias del proyecto

```
pip3 install -r requirements.txt
```

# Variables de entorno

ENV = desarrollo

```
export FLASK_APP=app.py
export FLASK_ENV=desarrollo
export FLASK_DEBUG=1
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_PORT=4000
```

ENV = produccion

```
export FLASK_APP=app.py
export FLASK_ENV=produccion
export FLASK_DEBUG=0
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_PORT=4000
```

RUN app

```
flask run
```

## Pruebas

Se debe configurar previamente segun estas variables de entorno
ENV = prueba

```
export FLASK_APP=app.py
export FLASK_ENV=prueba
export FLASK_DEBUG=0
export FLASK_RUN_HOST='host'
export FLASK_RUN_PORT=5000
```

Para correr las pruebas

```
pytest
```

## Docker

El contenedor de docker generado esta hecho para correr en el entorno de produccion asi que no olvides agregar la url de base de datos de producción al archivo .env

1. Compila la imagen según el docker file

```
docker build -t apicarreras:1.0 .
```

2. Corre el contenedor

```
docker run --rm --name api_carreras_container -d -p 5000:7000 apicarreras:1.0
```

## Documentación

Para ver la documentación en entornos de desarrollo de cada endpoint, dirigete a:

```
http://localhost:5000/api/v1/
```
