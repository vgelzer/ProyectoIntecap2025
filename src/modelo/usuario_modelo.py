from sqlalchemy import Integer, String, Enum
from sqlalchemy.orm import Mapped, mapped_column
from src.comun.utilidades import db


class UsuarioModelo(db.Model):
    __tablename__='usuario'
    codigo_usuario:Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    nombre:Mapped[str] = mapped_column(String(100),nullable=False)
    apellido:Mapped[str] = mapped_column(String(100),nullable=False)
    correo:Mapped[str] = mapped_column(String(100),nullable=False)
    contrasenia:Mapped[str] = mapped_column(String(60),nullable=False)
    rol: Mapped[str] = mapped_column(Enum("Administrador","General"), nullable=False)