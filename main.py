from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import shutil
from typing import Optional
from rag_chain import create_vector_store, create_chunks, get_response
from doc_parser import doctype
from langchain_core.documents import Document

app = FastAPI(title="AUTOLEGAL API", description="AI-powered legal document analysis and Q&A")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc", ".png", ".jpg", ".jpeg", ".txt"}

# Create uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    return any(filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS)

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "AUTOLEGAL API is running"}

@app.get("/api/status")
async def get_status():
    """Check if vector store exists"""
    try:
        vector_store_exists = os.path.exists("vectorstore/db_faiss")
        return {
            "vector_store_exists": vector_store_exists,
            "status": "success",
            "message": "Vector store exists" if vector_store_exists else "No vector store found"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking status: {str(e)}")

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload and process a document"""
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
        
        if not allowed_file(file.filename):
            raise HTTPException(
                status_code=400, 
                detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        # Save file
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process document
        try:
            doc = doctype(file_path)
            extracted_text = doc.to_text()
            
            if not extracted_text or extracted_text.strip() == "":
                raise HTTPException(status_code=400, detail="No text could be extracted from the document")
            
            # Create document chunks and vector store
            loaded_data = [Document(page_content=extracted_text)]
            text_chunks = create_chunks(loaded_data)
            vector_store = create_vector_store(text_chunks)
            
            if vector_store is not None:
                return {
                    "message": "File uploaded and processed successfully",
                    "filename": file.filename,
                    "status": "success",
                    "text_length": len(extracted_text)
                }
            else:
                raise HTTPException(status_code=500, detail="Failed to create vector store")
                
        except Exception as e:
            # Clean up uploaded file if processing fails
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.post("/api/query")
async def query_document(query: str = Form(...)):
    """Query the processed document"""
    try:
        # Check if vector store exists
        if not os.path.exists("vectorstore/db_faiss"):
            raise HTTPException(
                status_code=400, 
                detail="No documents have been processed yet. Please upload a document first."
            )
        
        if not query or query.strip() == "":
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Get response from RAG chain
        try:
            response = get_response(query)
            return {
                "result": response["result"],
                "status": "success",
                "query": query
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.delete("/api/reset")
async def reset_vector_store():
    """Reset the vector store (delete all processed documents)"""
    try:
        if os.path.exists("vectorstore"):
            shutil.rmtree("vectorstore")
        
        if os.path.exists(UPLOAD_FOLDER):
            shutil.rmtree(UPLOAD_FOLDER)
            os.makedirs(UPLOAD_FOLDER)
        
        return {
            "message": "Vector store and uploads reset successfully",
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resetting: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
