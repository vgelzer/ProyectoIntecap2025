

class TestTipo:

    ruta_general = '/api/v1/tipo'

    def test_tipo_seguridad(self,cliente):
        #prueba del endpoint get con autorizacion
        response = cliente.get(
            self.ruta_general
        )

        assert response.status_code == 401

        body = {
            "nombre":"Hada"
        }
        response2 = cliente.post(
            self.ruta_general,
            json = body
        )

        assert response2.status_code == 401


    def test_obtener_tipos(self, cliente, token_cliente_admin):

        response = cliente.get(
            self.ruta_general,
            headers={'Authorization': f'Bearer {token_cliente_admin}'}
        )

        assert response.status_code == 200
        assert len(response.get_json()) == 3

    def test_crear_tipo(self,cliente,token_cliente_admin):

        body = {
            "nombre":"Hada"
        }
        response = cliente.post(
            self.ruta_general,
            json = body,
            headers={'Authorization': f'Bearer {token_cliente_admin}'}
        )

        assert response.status_code == 200
        json = response.get_json()
        assert json['nombre'] == 'Hada'
        assert json['codigo_tipo'] == 4
    
    def test_actualizar_tipo(self,cliente,token_cliente_admin):
        '''
            Primero se inserta un tipo se espera 200
            Se cambia el nombre se espera un 200
        '''
        #insercion
        body = {
            "nombre":"Hada"
        }
        response = cliente.post(
            self.ruta_general,
            json = body,
            headers={'Authorization': f'Bearer {token_cliente_admin}'}
        )

        assert response.status_code == 200
        json = response.get_json()
        assert json['nombre'] == 'Hada'
        assert json['codigo_tipo'] == 4

        #actualizacion
        body = {
            "codigo_tipo":4,
            "nombre":"Legendario"
        }
        response = cliente.put(
            self.ruta_general,
            json = body,
            headers={'Authorization': f'Bearer {token_cliente_admin}'}
        )

        assert response.status_code == 200
        json = response.get_json()
        assert json['nombre'] == 'Legendario'
    
    def test_obtener_tipo_codigo(self,cliente, token_cliente_admin):

        codigo_tipo = 3
        response = cliente.get(
            f'{self.ruta_general}/codigo_tipo/{codigo_tipo}',
            headers={'Authorization': f'Bearer {token_cliente_admin}'}
        )

        assert response.status_code == 200
        json = response.get_json()
        assert json['nombre'] == 'Electrico'

        codigo_tipo = 10
        response = cliente.get(
            f'{self.ruta_general}/codigo_tipo/{codigo_tipo}',
            headers={'Authorization': f'Bearer {token_cliente_admin}'}
        )

        assert response.status_code == 404
    
    def test_eliminar_tipo(self,cliente,token_cliente_admin):
        codigo_tipo = 3
        response = cliente.delete(
            f'{self.ruta_general}/codigo_tipo/{codigo_tipo}',
            headers={'Authorization': f'Bearer {token_cliente_admin}'}
        )

        assert response.status_code == 204

