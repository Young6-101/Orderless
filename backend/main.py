from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
from typing import List

# Import your custom modules
from backend.file_processor.pdf_handler import extract_text_from_pdf
from backend.file_processor.ppt_handler import extract_text_from_pptx
from backend.file_processor.audio_handler import AudioTranscriber
from backend.rag_engine.vector_store import InspiraVault
from backend.reasoning.graph import app as reasoning_app

app = FastAPI(title="Inspira Backend API")

# --- CORS Configuration ---
# Allow requests from your frontend (localhost:5173 by default for Vite)
origins = [
    "http://localhost:5173",
    "http://localhost:3000",  # Just in case
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Data Models ---
class ChatRequest(BaseModel):
    question: str
    context: List[str] = [] # Optional context from frontend if needed

class ChatResponse(BaseModel):
    answer: str

# --- Endpoints ---

@app.get("/health")
async def health_check():
    """Simple endpoint to check if backend is running."""
    return {"status": "ok", "message": "Inspira Backend is running 🚀"}

# Supported audio extensions
AUDIO_EXTENSIONS = {".mp3", ".wav", ".flac", ".ogg", ".m4a", ".wma", ".aac", ".webm"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Endpoint for uploading files (PDFs, PPTs, Audio).
    1. Saves the file locally (temporarily).
    2. Extracts text using the appropriate handler.
    3. (TODO: In future steps) Embeds and stores text in Vector DB.
    """
    try:
        # 1. Create a temporary file path
        temp_file_path = f"temp_{file.filename}"
        
        # 2. Save the uploaded file to disk
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 3. Process the file based on type
        text_content = ""
        filename_lower = file.filename.lower()
        ext = os.path.splitext(filename_lower)[1]

        if ext == ".pdf":
            text_content = extract_text_from_pdf(temp_file_path)
        elif ext in (".pptx", ".ppt"):
            text_content = extract_text_from_pptx(temp_file_path)
        elif ext in AUDIO_EXTENSIONS:
            transcriber = AudioTranscriber()
            text_content = transcriber.transcribe(temp_file_path)
        else:
            os.remove(temp_file_path)
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {ext}. Supported: .pdf, .pptx, .ppt, {', '.join(sorted(AUDIO_EXTENSIONS))}"
            )
            
        # --- RAG Integration Point ---
        # vault = InspiraVault()
        # vault.add_document(text_content) 
        # -----------------------------
            
        # 4. Cleanup: Remove temp file
        os.remove(temp_file_path)
        
        if not text_content:
             return {"filename": file.filename, "message": "File uploaded but no text extracted (or empty)."}

        return {
            "filename": file.filename,
            "message": "File processed successfully!",
            "preview": text_content[:200] + "..."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Endpoint for chatting with the RAG engine.
    Uses the LangGraph workflow defined in reasoning/graph.py
    """
    try:
        # Use your LangGraph app to generate an answer
        # The graph expects a state with a 'question' key
        inputs = {"question": request.question, "context": request.context}
        
        # Invoke the graph
        result = reasoning_app.invoke(inputs)
        
        return {"answer": result['answer']}

    except Exception as e:
        # For now, return a mock response if RAG fails/isn't fully set up
        print(f"Error in chat endpoint: {e}")
        return {"answer": f"Backend Error: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    # Run the server
    uvicorn.run(app, host="0.0.0.0", port=8000)
