from src.comun.utilidades import ma
from marshmallow import fields, validate
from src.modelo.usuario_modelo import UsuarioModelo

class UsuarioEsquema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UsuarioModelo
        load_instance = True

    codigo_usuario = fields.Integer(
        required=True,
        validate = validate.Range(min=1),
        error_messages ={
            "required": "El campo es obligatorio."
            }
    )

    nombre = fields.String(
        required=True, 
        validate=validate.Length(
            min=1,
            max=100,
            error= "El campo debe tener un tamaño entre 1 a 100 carácteres"
        ),
        error_messages ={
            "required": "El campo es obligatorio."
            }
    )
    apellido = fields.String(
        required=True, 
        validate=validate.Length(
            min=1,
            max=100,
            error= "El campo debe tener un tamaño entre 1 a 100 carácteres"
        ),
        error_messages ={
            "required": "El campo es obligatorio."
            }
    )

    correo = fields.String(
        required=True, 
        validate=validate.Length(
            min=1,
            max=100,
            error= "El campo debe tener un tamaño entre 1 a 100 carácteres"
        ),
        error_messages ={
            "required": "El campo es obligatorio."
            }
    )
    contrasenia = fields.String(
        required=True, 
        validate=validate.Length(
            min=1,
            max=100,
            error= "El campo debe tener un tamaño entre 1 a 100 carácteres"
        ),
        error_messages ={
            "required": "El campo es obligatorio."
            }
    )


    rol = fields.String(
        required=True, 
        validate=validate.OneOf(["Administrador","General"]),
        error_messages ={
            "required": "El campo es obligatorio."
            }
    )

