from dotenv import load_dotenv
import os


class Configuracion():
    #cargar el archivo .env
    load_dotenv(override=True)

    #declarar las variables
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

class ConfiguracionPruebas(Configuracion):

    SQLALCHEMY_DATABASE_URI = "sqlite:///pokemon.db"