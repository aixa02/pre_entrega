# Validacion con Pydantic

Los modelos de Pydantic describen la forma de los datos que recibe o devuelve una API. Se definen creando clases que heredan de `BaseModel` y declarando campos con anotaciones de tipo.

Cuando un modelo Pydantic se usa como parametro del cuerpo de una funcion de ruta, FastAPI lee el JSON recibido, valida sus campos y entrega una instancia del modelo a la funcion.

Los campos obligatorios no tienen un valor predeterminado. Un campo opcional puede declararse usando un tipo que permita `None` y un valor predeterminado apropiado.

Si el cuerpo de la solicitud no cumple el esquema, FastAPI responde automaticamente con el estado HTTP 422 y detalles sobre los errores de validacion.
