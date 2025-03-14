from langchain_experimental.text_splitter import SemanticChunker
from langchain_ollama import OllamaEmbeddings
from db_pipeline import add_data

# ---------- Chunker Function ----------
def chunk(text):
    # Initialize Ollama embeddings
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")

    # Create the SemanticChunker with Ollama embeddings
    text_splitter = SemanticChunker(embeddings=embeddings)

    # Split the text into semantically similar chunks
    docs = text_splitter.create_documents([text])
    docs = [doc.page_content for doc in docs]
    return docs

# ---------- Adding Chunks To DB ----------
def chunks_to_db(db, chunks):
    chunks = [{'content':chunk} for chunk in chunks]
    add_data(db, chunks, ['content'])

