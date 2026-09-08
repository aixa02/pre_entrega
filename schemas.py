from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, SecretStr, field_validator, ValidationError


# ============================================================================
# ENUMS
# ============================================================================

class Provider(str, Enum):
    """Proveedores soportados"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"


# ============================================================================
# MODELOS
# ============================================================================

class ChatMessage(BaseModel):
    """Un mensaje en la conversación"""
    role: str = Field(description="'user', 'assistant' o 'system'")
    content: str = Field(..., min_length=1, description="Contenido del mensaje")
    
    @field_validator("role")
    @classmethod
    def rol_valido(cls, v: str) -> str:
        """Validar que role sea uno de los permitidos"""
        roles_permitidos = {"user", "assistant", "system"}
        if v not in roles_permitidos:
            raise ValueError(f"role debe ser uno de {roles_permitidos}, recibido: '{v}'")
        return v


class LLMConfig(BaseModel):
    """Configuración del cliente LLM"""
    provider: Provider
    model: str = Field(..., description="Nombre del modelo")
    
    openai_api_key: Optional[SecretStr] = None
    anthropic_api_key: Optional[SecretStr] = None
    google_api_key: Optional[SecretStr] = None
    
    temperature: float = Field(default=0.7, ge=0, le=2, description="Entre 0 y 2")
    max_tokens: int = Field(default=1024, gt=0, description="Mayor a 0")


class ModelResponse(BaseModel):
    """Respuesta del modelo"""
    provider: Provider
    model: str
    content: str
    error: Optional[str] = None



if __name__ == "__main__":
    #  VÁLIDO
    print("Creando config válida...")
    config = LLMConfig(
        provider=Provider.OPENAI,
        model="gpt-4o-mini",
        temperature=0.7
    )
    print(config)
    
    # INVÁLIDO: Temperatura > 2
    print("\n Intentando temperatura inválida...")
    try:
        config = LLMConfig(
            provider=Provider.OPENAI,
            model="gpt-4o-mini",
            temperature=5  # ¡Error!
        )
    except ValidationError as e:
        print("Se detectó el error ANTES de llamar a la API:\n", e)
    
    #  VÁLIDO: Mensaje
    print("\n Creando mensaje válido...")
    msg = ChatMessage(role="user", content="Hola")
    print(msg)
    
    #   INVÁLIDO: Role incorrecto
    print("\n Intentando role inválido...")
    try:
        msg = ChatMessage(role="admin", content="Hola")
    except ValidationError as e:
        print("Se detectó el error:\n", e)