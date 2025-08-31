# AUTOLEGAL - AI-Powered Legal Document Analysis

AUTOLEGAL is an intelligent document analysis system that uses RAG (Retrieval-Augmented Generation) to answer questions about legal documents. It combines document processing, vector embeddings, and AI language models to provide accurate, context-aware responses.

## Features

- **Multi-format Support**: PDF, DOCX, DOC, PNG, JPG, JPEG, TXT
- **Intelligent Text Extraction**: OCR for images, text parsing for documents
- **Vector-based Search**: FAISS vector database for efficient document retrieval
- **AI-powered Q&A**: Ollama integration for intelligent responses
- **Modern Web Interface**: React frontend with drag-and-drop file upload
- **FastAPI Backend**: High-performance Python backend with automatic API documentation

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│    │   FastAPI       │    │   RAG Chain     │
│                 │◄──►│   Backend       │◄──►│   + Ollama      │
│   - File Upload │    │   - File Upload │    │   - Document    │
│   - Q&A Interface│   │   - Processing  │    │     Processing  │
│   - Real-time   │    │   - API Endpoints│   │   - Vector DB   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Prerequisites

- Python 3.8+
- Node.js 16+
- Ollama (for AI model)
- Tesseract OCR (for image processing)

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd AUTOLEGAL
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Ollama
- **Windows**: Download from [ollama.ai](https://ollama.ai)
- **macOS**: `brew install ollama`
- **Linux**: `curl -fsSL https://ollama.ai/install.sh | sh`

### 4. Pull AI Model
```bash
ollama pull llama3.2:1b
# or any other model you prefer
```

### 5. Install Frontend Dependencies
```bash
cd frontend
npm install
```

## Usage

### 1. Start the Backend
```bash
# From the root directory
python main.py
```
The FastAPI server will start on `http://localhost:8000`

### 2. Start the Frontend
```bash
# From the frontend directory
npm start
```
The React app will open on `http://localhost:3000`

### 3. Use the Application
1. **Upload a Document**: Drag and drop or click to select a legal document
2. **Wait for Processing**: The system will extract text and create vector embeddings
3. **Ask Questions**: Type questions about your document and get AI-powered answers
4. **Reset**: Clear the current document and start over

## API Endpoints

- `GET /` - Health check
- `GET /api/status` - Check vector store status
- `POST /api/upload` - Upload and process documents
- `POST /api/query` - Query processed documents
- `DELETE /api/reset` - Reset vector store

## Configuration

### Environment Variables
Create a `.env` file in the root directory:
```env
OLLAMA_MODEL=llama3.2:1b
DB_FAISS_PATH=vectorstore/db_faiss
```

### Model Configuration
Edit `rag_chain.py` to change the AI model:
```python
OLLAMA_MODEL = "llama3.2:1b"  # Change to your preferred model
```

## Supported File Types

| Format | Description | Processing Method |
|--------|-------------|-------------------|
| PDF    | Portable Document Format | PDF to image + OCR |
| DOCX   | Microsoft Word Document | Convert to PDF + OCR |
| DOC    | Legacy Word Document | Convert to PDF + OCR |
| PNG    | Portable Network Graphics | Direct OCR |
| JPG    | JPEG Image | Direct OCR |
| JPEG   | JPEG Image | Direct OCR |
| TXT    | Plain Text | Direct text extraction |

## Troubleshooting

### Common Issues

1. **Ollama Connection Error**
   - Ensure Ollama is running: `ollama serve`
   - Check if the model is downloaded: `ollama list`

2. **OCR Errors**
   - Install Tesseract OCR
   - Windows: Download from GitHub releases
   - macOS: `brew install tesseract`
   - Linux: `sudo apt-get install tesseract-ocr`

3. **Vector Store Errors**
   - Check if `vectorstore/db_faiss` directory exists
   - Ensure sufficient disk space
   - Try resetting the vector store

4. **Frontend Connection Issues**
   - Verify backend is running on port 8000
   - Check CORS configuration
   - Ensure no firewall blocking

### Performance Tips

- Use smaller AI models for faster responses
- Process documents during off-peak hours
- Monitor memory usage with large documents
- Consider using GPU acceleration for embeddings

## Development

### Project Structure
```
AUTOLEGAL/
├── main.py              # FastAPI backend
├── rag_chain.py         # RAG chain implementation
├── doc_parser.py        # Document processing
├── requirements.txt     # Python dependencies
├── frontend/           # React frontend
│   ├── src/
│   ├── public/
│   └── package.json
└── README.md
```

### Adding New Features
1. **Backend**: Add new endpoints in `main.py`
2. **Frontend**: Create new components in `frontend/src/`
3. **RAG Chain**: Extend functionality in `rag_chain.py`
4. **Document Types**: Add support in `doc_parser.py`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Check the troubleshooting section
- Review the API documentation at `http://localhost:8000/docs`
- Open an issue on GitHub

## Acknowledgments

- LangChain for RAG framework
- FAISS for vector similarity search
- Ollama for local AI models
- React for the frontend framework
- FastAPI for the backend framework
