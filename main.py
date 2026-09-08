import asyncio
from typing import List
from dotenv import load_dotenv
import os
from pydantic import SecretStr

from schemas import ChatMessage, LLMConfig, Provider
from async_llm_manager import AsyncLLMManager


async def main():
    # Cargar variables de entorno
    load_dotenv()
    
    # Obtener API keys
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    google_key = os.getenv("GOOGLE_API_KEY")
 
    provider = Provider.GEMINI  # o Provider.ANTHROPIC o Provider.GEMINI
    
    # Crear configuración
    config = LLMConfig(
        provider=provider,
        model="gemini-3.6-flash", 
        openai_api_key=SecretStr(openai_key) if openai_key else None,
        anthropic_api_key=SecretStr(anthropic_key) if anthropic_key else None,
        google_api_key=SecretStr(google_key) if google_key else None,
        temperature=0.7,
        max_tokens=1024,
    )
    
    # Crear manager
    manager = AsyncLLMManager(config)
    
    # Mensaje de prueba
    historial = [
        ChatMessage(role="user", content="¿Qué es la entropía?")
    ]
    
    # ========== MODO NORMAL ==========
    print("=" * 60)
    print("📋 MODO NORMAL (respuesta completa)")
    print("=" * 60)
    
    respuesta = await manager.generate(historial)
    
    if respuesta.error:
        print(f"❌ Error: {respuesta.error}")
    else:
        print(f"🤖 {respuesta.model}:")
        print(respuesta.content)
    
    # ========== MODO STREAMING ==========
    print("\n" + "=" * 60)
    print("🔄 MODO STREAMING (token por token)")
    print("=" * 60)
    print("🤖 ", end="", flush=True)
    
    async for token in manager.generate_stream(historial):
        print(token, end="", flush=True)
    
    print("\n" + "=" * 60)
    print("✅ Prueba completada")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())