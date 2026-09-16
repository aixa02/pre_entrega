import asyncio
import logging

from chain import process_text

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

async def main() -> None:
    """Script de prueba del pipeline de extracción técnica."""
    texto = """
    La API desplegada con FastAPI utiliza PostgreSQL y Redis. Durante el último
    despliegue, el servicio comenzó a responder con errores 503 porque Redis
    agotó la memoria disponible y aumentó la latencia de las solicitudes.
    """

    resultado = await process_text(texto)
    print(resultado.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())