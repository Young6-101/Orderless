import torch
from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
from PIL import Image

class InspiraEmbedder:
    def __init__(self, model_name: str = "BAAI/bge-m3"):
        """
        Initializes the embedding model with hardware acceleration.
        """
        # Determine the best device available
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"--- [LOG] Using device: {device.upper()} ---")
        
        print(f"--- [LOG] Loading embedding model: {model_name} ---")
        self.model = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'device': device}, 
            encode_kwargs={'normalize_embeddings': True}
        )
        print("--- [LOG] Model loaded and ready! ---")

    def get_embeddings(self, text_chunks: list[str]):
        """
        Converts text fragments into vectors using GPU acceleration.
        """
        print(f"--- [LOG] Vectorizing {len(text_chunks)} chunks on GPU... ---")
        return self.model.embed_documents(text_chunks)

class MultimodalEmbedder:
    def __init__(self, model_name: str = "jinaai/jina-clip-v1"):
        """
        Initializes the multimodal embedding model with hardware acceleration.
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"--- [LOG] Loading multimodal embedding model: {model_name} on device: {self.device.upper()} ---")

        self.model = SentenceTransformer(model_name, trust_remote_code=True, device=self.device)

    def embed_text(self, text: str):
        """
        Embeds a single text input.
        """
        print(f"--- [LOG] Embedding text on {self.device.upper()} ---")
        return self.model.encode([text])[0]
    
    def embed_image(self, image_path: str):
        """
        Embeds an image input.
        """
        print(f"--- [LOG] Embedding image on {self.device.upper()} ---")
        image = Image.open(image_path).convert("RGB")
        return self.model.encode([image])[0]