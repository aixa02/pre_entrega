# Pipeline de Extracción de Entidades Técnicas

Pipeline asíncrono construido con LangChain y LCEL. Recibe un texto técnico sin
procesar y devuelve un objeto validado con:

- `tecnologias`: lista no vacía de tecnologías detectadas.
- `nivel_de_criticidad`: `baja`, `media` o `alta`.
- `resumen_tecnico`: resumen breve del contenido.

## Estructura

- `schemas.py`: contrato de salida con Pydantic.
- `chain.py`: prompt, modelo, salida estructurada y reintentos.
- `main.py`: mini-script de prueba asíncrono.

## Preparación

```bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

Copiá `.env.example` como `.env` y completá `GOOGLE_API_KEY`.

## Ejecución

```bash
venv/Scripts/python.exe main.py
```

El flujo usará `ChatPromptTemplate`, `with_structured_output()` y `with_retry()`.
La respuesta final será un objeto Pydantic validado.