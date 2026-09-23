# Rutas y parametros en FastAPI

Una ruta combina un metodo HTTP con un path. Por ejemplo, `@app.get('/items/{item_id}')` define una operacion GET con un parametro de path llamado `item_id`.

Los parametros incluidos en el path son obligatorios. FastAPI los convierte al tipo indicado en la anotacion de la funcion y devuelve un error de validacion si el valor no es compatible.

Los parametros de query se declaran como argumentos que no forman parte del path. En `def list_items(skip: int = 0, limit: int = 10)`, `skip` y `limit` son parametros de query con valores predeterminados.

El orden de los parametros no cambia la URL. Para evitar ambiguedades, las rutas estaticas deben declararse antes que las rutas parametrizadas cuando ambas podrian coincidir.
