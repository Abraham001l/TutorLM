from langchain_experimental.text_splitter import SemanticChunker
from langchain_ollama import OllamaEmbeddings

# ---------- Ollama Encoder ----------
def chunk(text):
    # Initialize Ollama embeddings
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")

    # Create the SemanticChunker with Ollama embeddings
    text_splitter = SemanticChunker(embeddings=embeddings)

    # Split the text into semantically similar chunks
    docs = text_splitter.create_documents([text])
    docs = [doc.page_content for doc in docs]
    return docs