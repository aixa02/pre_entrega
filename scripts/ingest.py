# scripts/ingest.py
import os
import chromadb
from chromadb.utils import embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
import re

class DocumentIngester:
    def __init__(self, vectorstore_path: str = "./vectorstore"):
        """Inicializa ChromaDB y el splitter."""
        self.vectorstore_path = vectorstore_path
        
        # Conectar a ChromaDB persistente
        self.client = chromadb.PersistentClient(path=vectorstore_path)
        
        # Crear/obtener colección con embeddings default
        self.collection = self.client.get_or_create_collection(
            name="documentos",
            embedding_function=embedding_functions.DefaultEmbeddingFunction(),
            metadata={"hnsw:space": "cosine"}
        )
        
        # Configurar splitter: 500 tokens, overlap 50
        def token_counter(text: str) -> int:
            # Aproximación: 1 token ≈ 4 caracteres
            return len(text) // 4
        
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            length_function=token_counter,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def load_documents(self, data_path: str = "./data") -> list:
        """Lee todos los archivos .txt y .md de una carpeta."""
        documents = []
        
        for file in Path(data_path).glob("*"):
            if file.suffix in [".txt", ".md"]:
                print(f"📖 Leyendo: {file.name}")
                with open(file, "r", encoding="utf-8") as f:
                    content = f.read()
                    documents.append({
                        "content": content,
                        "source": file.name
                    })
        
        return documents
    
    def clean_text(self, text: str) -> str:
        """Limpia espacios y saltos de línea duplicados."""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n+', '\n', text)
        return text.strip()
    
    def ingest(self, data_path: str = "./data"):
        """Pipeline completo: carga → limpia → fragmenta → indexa."""
        
        # 1. Cargar documentos
        documents = self.load_documents(data_path)
        if not documents:
            print("❌ No se encontraron documentos en ./data")
            return
        
        # 2. Procesar y fragmentar
        all_chunks = []
        chunk_ids = []
        chunk_metadatas = []
        
        for doc_idx, doc in enumerate(documents):
            # Limpiar
            cleaned = self.clean_text(doc["content"])
            
            # Fragmentar
            chunks = self.splitter.split_text(cleaned)
            
            # Crear IDs únicos y metadatos
            for chunk_idx, chunk in enumerate(chunks):
                chunk_id = f"{doc['source']}_chunk_{chunk_idx}"
                chunk_ids.append(chunk_id)
                all_chunks.append(chunk)
                chunk_metadatas.append({
                    "source": doc["source"],
                    "chunk_index": chunk_idx
                })
        
        # 3. Indexar en ChromaDB
        print(f"\n⏳ Indexando {len(all_chunks)} fragmentos...")
        self.collection.upsert(
            ids=chunk_ids,
            documents=all_chunks,
            metadatas=chunk_metadatas
        )
        
        print(f"✅ Base de datos creada: {len(all_chunks)} fragmentos en {self.vectorstore_path}")
        print(f"   Documentos procesados: {len(documents)}")

if __name__ == "__main__":
    ingester = DocumentIngester(vectorstore_path="./vectorstore")
    ingester.ingest(data_path="./data")