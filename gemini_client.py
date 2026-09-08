from typing import AsyncGenerator, List
from google import genai
from google.genai import types
from schemas import ChatMessage, ModelResponse, LLMConfig, Provider
from base_client import BaseLLMClient


class GeminiClient(BaseLLMClient):
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        
        if not config.google_api_key:
            raise ValueError("google_api_key es requerida")
        
        api_key = config.google_api_key.get_secret_value()
        self._client = genai.Client(api_key=api_key)

    def _convertir_mensajes(self, messages: List[ChatMessage]):
        """Gemini separa el system prompt del resto, y llama 'model' al rol del asistente."""
        contents = []
        system_instruction = None
        for m in messages:
            if m.role == "system":
                system_instruction = m.content
            else:
                rol_gemini = "model" if m.role == "assistant" else "user"
                contents.append(types.Content(role=rol_gemini, parts=[types.Part(text=m.content)]))
        return contents, system_instruction

    async def generate(self, messages: List[ChatMessage]) -> ModelResponse:
        try:
            contents, system_instruction = self._convertir_mensajes(messages)
            response = await self._client.aio.models.generate_content(
                model=self.model,
                contents=contents,
                config=types.GenerateContentConfig(
                    temperature=self.temperature,
                    max_output_tokens=self.max_tokens,
                    system_instruction=system_instruction,
                ),
            )
            return ModelResponse(
                provider=Provider.GEMINI,
                model=self.model,
                content=response.text
            )
        except Exception as e:
            return ModelResponse(
                provider=Provider.GEMINI,
                model=self.model,
                content="",
                error=f"Error de la API de Gemini: {e}"
            )

    async def generate_stream(self, messages: List[ChatMessage]) -> AsyncGenerator[str, None]:
        try:
            contents, system_instruction = self._convertir_mensajes(messages)
            stream = await self._client.aio.models.generate_content_stream(
                model=self.model,
                contents=contents,
                config=types.GenerateContentConfig(
                    temperature=self.temperature,
                    max_output_tokens=self.max_tokens,
                    system_instruction=system_instruction,
                ),
            )
            async for chunk in stream:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            yield f"\n[⚠️ Error durante el streaming: {e}]"