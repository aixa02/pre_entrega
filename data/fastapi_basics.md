# FastAPI: conceptos basicos

FastAPI es un framework de Python para construir APIs web. Esta basado en Starlette para las capacidades web y utiliza Pydantic para validar datos.

Una aplicacion minima se crea instanciando `FastAPI` y definiendo funciones asociadas a rutas HTTP mediante decoradores como `@app.get` y `@app.post`.

FastAPI genera automaticamente una especificacion OpenAPI. La documentacion interactiva esta disponible en `/docs` y una segunda interfaz basada en ReDoc esta disponible en `/redoc`.

Las funciones de ruta pueden ser sincronas o asincronas. Las funciones asincronas se definen con `async def` y pueden usar `await` para operaciones de entrada y salida no bloqueantes.
