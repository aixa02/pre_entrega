import logging

from dotenv import load_dotenv
from langchain_core.exceptions import OutputParserException
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import ValidationError

from schemas import EntidadesTecnicas

load_dotenv()

logger = logging.getLogger("pipeline_extraccion")

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        Sos un analista de arquitectura y soporte técnico.
        Extraé las entidades técnicas del texto recibido y evaluá su criticidad.
        Respondé respetando estrictamente el esquema estructurado solicitado.
        Si no se mencionan tecnologías explícitas, usá una descripción técnica concreta
        como tecnología detectada, sin inventar nombres de herramientas.
        """,
    ),
    (
        "human",
        "Texto técnico para analizar:\n\n{texto}",
    ),
])

modelo = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0,
)

chain = prompt | modelo.with_structured_output(EntidadesTecnicas)

chain_con_reintentos = chain.with_retry(
    retry_if_exception_type=(ValidationError, OutputParserException),
    stop_after_attempt=2,
)


async def process_text(text: str) -> EntidadesTecnicas:
    """Extrae y valida entidades técnicas desde un texto sin procesar."""
    logger.info("Procesando texto técnico (%d caracteres)", len(text))

    try:
        resultado = await chain_con_reintentos.ainvoke({"texto": text})
        logger.info("Extracción validada: %s", resultado.model_dump())
        return resultado
    except Exception:
        logger.exception("Falló la extracción después de los reintentos")
        raise
