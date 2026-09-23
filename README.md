# Flujo RAG End-to-End con FastAPI

Este proyecto implementa un flujo completo de Retrieval-Augmented Generation (RAG) usando documentos sobre FastAPI como base de conocimiento.

El sistema:

1. Lee archivos `.md` y `.txt` desde `data/`.
2. Limpia y divide los documentos en fragmentos de 500 tokens con 50 tokens de solapamiento.
3. Guarda los fragmentos y sus embeddings en una colección persistente de ChromaDB.
4. Recupera los fragmentos más relevantes para una pregunta.
5. Genera una respuesta con Gemini usando únicamente el contexto recuperado.
6. Devuelve una respuesta Pydantic con el texto generado y las referencias utilizadas.

Si la información no aparece en los documentos, el sistema responde:

> No lo sé, esa información no está en mis documentos

## Estructura del proyecto

```text
pre_entrega/
├── data/
│   ├── errors.md
│   ├── fastapi_basics.md
│   ├── routing.md
│   └── validation.md
├── scripts/
│   ├── ingest.py
│   ├── retriever.py
│   └── rag_chain.py
├── vectorstore/          # Se genera localmente y no se sube a Git
├── .env                  # Claves locales, no se versiona
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Requisitos

- Python 3.10 o superior.
- Una clave de Google Gemini.

## Instalacion

Desde la carpeta raiz del proyecto, crear y activar el entorno virtual.

En Windows PowerShell:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

En Git Bash:

```bash
python -m venv venv
source venv/Scripts/activate
```

Instalar las dependencias:

```bash
python -m pip install -r requirements.txt
```

## Configuracion de variables de entorno

Crear `.env` a partir de `.env.example` y completar la clave de Gemini:

```env
GOOGLE_API_KEY=tu_clave_de_gemini
```

El archivo `.env` esta excluido por `.gitignore`. No incluir claves reales en el repositorio.

## Ingesta de documentos

Ejecutar desde la raiz del proyecto:

```bash
venv/Scripts/python.exe scripts/ingest.py
```

La primera ejecucion crea `vectorstore/` y la coleccion persistente `documentos` en ChromaDB. Si se agregan o modifican documentos, se puede eliminar `vectorstore/` y volver a ejecutar la ingesta para reconstruir la base.

## Ejecutar el flujo RAG

```bash
venv/Scripts/python.exe scripts/rag_chain.py
```

El script ejecuta dos pruebas:

- Una pregunta cuya respuesta esta en `data/validation.md`.
- Una pregunta trampa cuya respuesta no esta en ningun documento.

La salida tiene este formato Pydantic:

```json
{
  "answer": "...",
  "references": ["validation.md"]
}
```

## Componentes principales

### `scripts/ingest.py`

Carga documentos, los limpia, aplica `RecursiveCharacterTextSplitter` con 500 tokens de tamaño y 50 tokens de solapamiento, y los persiste en ChromaDB.

### `scripts/retriever.py`

Consulta la colección `documentos` y recupera hasta 3 fragmentos relevantes, con un máximo de 5 para evitar un contexto excesivo.

### `scripts/rag_chain.py`

Construye la cadena LCEL con `ChatPromptTemplate`, `ChatGoogleGenerativeAI` y `PydanticOutputParser`. La función asíncrona `get_rag_response(query)` devuelve la respuesta y las fuentes utilizadas.

## Grounding

El prompt instruye al modelo a responder exclusivamente con el contexto recuperado. Si la respuesta no está en esos fragmentos, debe devolver la frase de desconocimiento y una lista de referencias vacía.
