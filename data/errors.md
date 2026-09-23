# Errores y respuestas en FastAPI

Para informar un error controlado desde una ruta se puede lanzar `HTTPException`. La excepcion recibe un codigo de estado HTTP y un detalle que explica el problema.

Una respuesta 404 indica que el recurso solicitado no fue encontrado. Una respuesta 400 representa una solicitud invalida y una respuesta 401 indica que la autenticacion es necesaria o no fue aceptada.

El codigo de estado de una respuesta exitosa puede configurarse en el decorador de la ruta mediante el argumento `status_code`.

FastAPI permite declarar un `response_model` para validar y filtrar los datos que se envian al cliente. Esto ayuda a evitar que informacion interna del servidor forme parte de la respuesta publica.
