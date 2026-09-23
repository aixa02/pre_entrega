# scripts/retriever.py
import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict

class VectorRetriever:
    def __init__(self, vectorstore_path: str = "./vectorstore"):
        """Conecta con ChromaDB existente."""
        self.client = chromadb.PersistentClient(path=vectorstore_path)
        self.collection = self.client.get_collection(
            name="documentos",
            embedding_function=embedding_functions.DefaultEmbeddingFunction()
        )
    
    def retrieve(self, query: str, top_k: int = 3) -> Dict:
        """
        Busca los fragmentos más relevantes para una query.
        
        Args:
            query: Pregunta del usuario
            top_k: Número de resultados (máx 5 para evitar "Lost in the Middle")
        
        Returns:
            Dict con documentos y metadatos
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=min(top_k, 5)  # Máximo 5 para evitar degradación
        )
        
        # Reformatear para mejor legibilidad
        formatted_results = {
            "documents": results["documents"][0] if results["documents"] else [],
            "metadatas": results["metadatas"][0] if results["metadatas"] else [],
            "distances": results["distances"][0] if results["distances"] else []
        }
        
        return formatted_results

if __name__ == "__main__":
    retriever = VectorRetriever()
    
    # Test
    query = "¿Qué estado HTTP devuelve FastAPI cuando el cuerpo no cumple el esquema?"
    results = retriever.retrieve(query, top_k=3)
    
    print(f"\n🔍 Query: {query}\n")
    for i, (doc, meta, dist) in enumerate(zip(
        results["documents"], 
        results["metadatas"], 
        results["distances"]
    ), 1):
        print(f"{i}. [{meta['source']}] (similitud: {1-dist:.2%})")
        print(f"   {doc[:100]}...\n")