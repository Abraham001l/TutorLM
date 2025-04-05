from langchain_experimental.text_splitter import SemanticChunker
from langchain_ollama import OllamaEmbeddings
from vectordb_pipeline import add_data

# ---------- Chunker Function ----------
def chunk(text):
    """
    Parameters:
    text (string): text which will be split into chunks

    Returns:
    docs (list<string>): A list of chunks(strings) which the text has been split into
    """
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
    chunks = [{'data':chunk} for chunk in chunks]
    add_data(db, chunks, ['content'])

