import chromadb
from backend.rag_engine.embedder import InspiraEmbedder, MultimodalEmbedder
from typing import Optional

class InspiraVault:
    def __init__(self, db_path="./inspira_db"):
        """
        Initializes the persistent vector database.
        """
        # 1. Create a local database client
        self.client = chromadb.PersistentClient(path=db_path)
        
        # 2. text
        self.text_embedder = InspiraEmbedder()
        self.text_collection = self.client.get_or_create_collection(name="text_inspiration")

        # 3. multimodal
        self.vision_embedder = MultimodalEmbedder()
        self.vision_collection = self.client.get_or_create_collection(name="vision_inspiration")

    # text input
    def store_clarity(self, chunks: list[str], metadata: Optional[list[dict]] = None):
        """
        Takes raw chunks, embeds them, and saves to local storage.
        """
        # Generate unique IDs for each chunk
        ids = [f"id_{i}" for i in range(len(chunks))]
        
        # Convert chunks to vectors
        embeddings = self.text_embedder.get_embeddings(chunks)
        
        # Save to database
        self.text_collection.add(
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadata or [{"source": "pdf_upload"}] * len(chunks),
            ids=ids
        )
        print(f"--- [LOG] Successfully stored {len(chunks)} fragments into the Vault. ---")

    def search_clarity(self, query: str, top_k: int = 3):
        """
        Search for the most relevant fragments from the vault.
        query: The user's natural language question.
        top_k: Number of fragments to retrieve.
        """
        # Convert the query into a vector using the same GPU-accelerated embedder
        query_vector = self.text_embedder.get_embeddings([query])[0]
        
        # Query the collection
        results = self.text_collection.query(
            query_embeddings=[query_vector],
            n_results=top_k
        )
        
        # Return the retrieved text fragments
        return results['documents'][0]
    
    def store_vision(self, image_paths: list[str], metadata: Optional[list[dict]] = None):
        """
        Takes image paths, embeds them, and saves to local storage.
        """
        ids = []
        embeddings = []
        
        for idx, image_path in enumerate(image_paths):
            vector = self.vision_embedder.embed_image(image_path)
            ids.append(f"image_{idx}")
            embeddings.append(vector.tolist())

        self.vision_collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadata or [{"source": "image_upload"}] * len(image_paths)
        )
        print(f"--- [LOG] Successfully stored {len(image_paths)} images into the Vault. ---")
    
    def search_vision(self, query_text: str, top_k: int = 2):
        """
        Search for the most relevant images from the vault using text query.
        query_text: The user's text query.
        top_k: Number of images to retrieve.
        """
        query_vector = self.vision_embedder.embed_text(query_text)
        
        results = self.vision_collection.query(
            query_embeddings=[query_vector.tolist()],
            n_results=top_k
        )
        
        return results['ids'][0] if results['ids'] else []