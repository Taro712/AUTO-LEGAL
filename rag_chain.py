from doc_parser import doctype
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from langchain_ollama import OllamaLLM
from langchain_core.documents import Document
from dotenv import load_dotenv
import torch
import os

load_dotenv()

DATA_PATH = "data/input.img"
DB_FAISS_PATH = "vectorstore/db_faiss"
OLLAMA_MODEL = "llama3.2:1b"

# tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
# model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
ollama = OllamaLLM(model = OLLAMA_MODEL)


def load_data(data_path):
    loader = DirectoryLoader(data_path, glob="*.img", loader_cls=doctype)
    documents = loader.load()
    return documents


def create_chunks(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=750, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)
    return chunks


def create_vector_store(text_chunks):
    embeddings = None
    try:
        embeddings = HuggingFaceEmbeddings(
                model_name="all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'}
            )
        print("Using HuggingFace embeddings")
    except Exception as e:
            print(f"HuggingFace embeddings failed: {e}")
            return None  # or raise an exception
    
    # Only proceed if we have valid embeddings
    if embeddings is not None:
        try:
            vector_store = FAISS.from_documents(text_chunks, embeddings)
            vector_store.save_local(DB_FAISS_PATH)
            return vector_store
        except Exception as e:
            print(f"Failed to create vector store: {e}")
            return None
    else:
        print("No embeddings available - cannot create vector store")
        return None
    

#GENERATE RESPONSE
def get_response(query):
    # Load embeddings and the vector store
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)

    # Retrieve relevant documents
    retriever = db.as_retriever(search_kwargs={"k": 2})
    docs = retriever.invoke(query)
    
    # Combine document contents to form the context
    context = " ".join([doc.page_content for doc in docs])

    # Create the prompt for the model
    prompt = f"""You are a helpful assistant. Use the provided context to answer the question accurately and concisely.

Context: {context}

Question: {query}

Answer:"""
    response_text = ollama.invoke(prompt)
    return {"result": response_text}



# MAIN SCANNING AND EMBEDDING
if __name__ == "__main__":
    file_path = input("enter a file:")
    if not os.path.isfile(file_path):
        print("File does not exist.")
    else:
        try:
            doc = doctype(file_path)
            extracted_text = doc.to_text()
            loaded_data = [Document(page_content=extracted_text)]
            text_chunks = create_chunks(loaded_data)
            data = create_vector_store(text_chunks)
            if data is not None:
                while True:
                    print("enter exit if you want to exit")
                    query = input("enter a query:")
                    if query == "exit":
                        break
                    else:
                        response = get_response(query)
                        print(response["result"])
            else:
                print("failed to load vetor store")
        except Exception as e:
            print(f"error processing files:{e}")