import logging
from typing import AsyncGenerator, List
from schemas import ChatMessage, ModelResponse, LLMConfig, Provider
from base_client import BaseLLMClient
from openai_client import OpenAIClient
from anthropic_client import AnthropicClient
from gemini_client import GeminiClient


logger = logging.getLogger(__name__)


class AsyncLLMManager:
    """
    Manager universal para clientes LLM.
    Crea el cliente correspondiente según el proveedor y delega las llamadas.
    
    Ejemplo:
        config = LLMConfig(
            provider=Provider.OPENAI,
            model="gpt-4",
            openai_api_key=SecretStr("sk-...")
        )
        manager = AsyncLLMManager(config)
        
        historial = [ChatMessage(role="user", content="Hola")]
        respuesta = await manager.generate(historial)
    """
    
    def __init__(self, config: LLMConfig):
        """
        Inicializar el manager.
        
        Args:
            config: LLMConfig con la configuración
            
        Raises:
            ValueError: Si el proveedor no es soportado o falta la API key
        """
        self.config = config
        self._client: BaseLLMClient = self._crear_cliente()
        logger.info(f"✅ AsyncLLMManager inicializado con {config.provider.value}")
    
    def _crear_cliente(self) -> BaseLLMClient:
        """
        Factory: crear el cliente correcto según el proveedor.
        
        Returns:
            Cliente LLM específico del proveedor
            
        Raises:
            ValueError: Si proveedor no soportado o falta API key
        """
        if self.config.provider == Provider.OPENAI:
            if not self.config.openai_api_key:
                raise ValueError("❌ Falta openai_api_key en la configuración")
            logger.debug("🔧 Creando OpenAIClient")
            return OpenAIClient(self.config)
        
        elif self.config.provider == Provider.ANTHROPIC:
            if not self.config.anthropic_api_key:
                raise ValueError("❌ Falta anthropic_api_key en la configuración")
            logger.debug("🔧 Creando AnthropicClient")
            return AnthropicClient(self.config)
        
        elif self.config.provider == Provider.GEMINI:
            if not self.config.google_api_key:
                raise ValueError("❌ Falta google_api_key en la configuración")
            logger.debug("🔧 Creando GeminiClient")
            return GeminiClient(self.config)
        
        else:
            raise ValueError(
                f"❌ Proveedor no soportado: {self.config.provider}. "
                f"Soportados: {[p.value for p in Provider]}"
            )
    
    async def generate(self, messages: List[ChatMessage]) -> ModelResponse:
        """
        Generar una respuesta completa.
        
        Args:
            messages: Historial de mensajes
            
        Returns:
            ModelResponse con la respuesta
        """
        logger.debug(f"📤 Generando respuesta con {self.config.provider.value}")
        return await self._client.generate(messages)
    
    async def generate_stream(self, messages: List[ChatMessage]) -> AsyncGenerator[str, None]:
        """
        Generar una respuesta en streaming.
        
        Args:
            messages: Historial de mensajes
            
        Yields:
            Tokens individuales
        """
        logger.debug(f"🔄 Iniciando streaming con {self.config.provider.value}")
        async for chunk in self._client.generate_stream(messages):
            yield chunk
    
    def cambiar_proveedor(self, config: LLMConfig) -> None:
        """
        Cambiar el proveedor en tiempo de ejecución.
        
        Args:
            config: Nueva configuración
        """
        logger.info(f"🔀 Cambiando proveedor a {config.provider.value}")
        self.config = config
        self._client = self._crear_cliente()