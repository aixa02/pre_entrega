# scripts/rag_chain.py
import asyncio
from typing import List

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from scripts.retriever import VectorRetriever

load_dotenv()


class RAGResponse(BaseModel):
    answer: str = Field(description="Respuesta grounded para la pregunta del usuario")
    references: List[str] = Field(
        description="Archivos del contexto utilizados para construir la respuesta"
    )


class RAGChain:
    def __init__(self, model_name: str = "gemini-3.6-flash"):
        self.retriever = VectorRetriever()
        self.llm = ChatGoogleGenerativeAI(model=model_name, temperature=0)
        self.output_parser = PydanticOutputParser(pydantic_object=RAGResponse)
        
        # Prompt del sistema: filtro de veracidad
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """Eres un asistente técnico especializado.

INSTRUCCIONES:
1. Responde SOLO basándote en el CONTEXTO proporcionado
2. Si la respuesta NO está en el contexto, di exactamente: "No lo sé, esa información no está en mis documentos"
3. No inventes información ni uses conocimiento externo
4. Sé conciso y técnico
5. En `references`, incluye únicamente los nombres de archivos que aparecen en el contexto y que utilizaste

{format_instructions}

CONTEXTO:
{context}
"""),
            ("human", "{question}")
        ])
        
        # Cadena LCEL
        self.chain = self.prompt | self.llm | self.output_parser
    
    async def get_rag_response(self, query: str) -> RAGResponse:
        """Genera respuesta usando el contexto recuperado."""
        
        # 1. Recuperar documentos relevantes
        print(f"🔍 Buscando contexto para: {query}")
        retrieved = self.retriever.retrieve(query, top_k=3)
        
        # 2. Formatear contexto
        context = "\n\n".join([
            f"[{meta['source']}]\n{doc}"
            for doc, meta in zip(retrieved["documents"], retrieved["metadatas"])
        ])
        
        # 3. Generar respuesta asincronamente
        print("⏳ Generando respuesta...")
        response = await self.chain.ainvoke({
            "context": context,
            "question": query,
            "format_instructions": self.output_parser.get_format_instructions(),
        })
        
        return response


async def get_rag_response(query: str) -> RAGResponse:
    """Atajo publico para consultar el sistema RAG de forma asincrona."""
    return await RAGChain().get_rag_response(query)


async def main():
    """Test del sistema RAG."""
    rag = RAGChain()
    
    # Test queries
    queries = [
        "¿Qué estado HTTP devuelve FastAPI cuando el cuerpo no cumple el esquema?",
        "¿Quién creó FastAPI?"  # Query que NO está en documentos
    ]
    
    for query in queries:
        print(f"\n{'='*60}")
        print(f"📌 PREGUNTA: {query}")
        print(f"{'='*60}")
        
        response = await rag.get_rag_response(query)
        print(f"\n💬 RESPUESTA:\n{response}\n")

if __name__ == "__main__":
    asyncio.run(main())