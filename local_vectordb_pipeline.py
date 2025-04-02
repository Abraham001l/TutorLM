from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

# ---------- Local Store Creation Function ----------
def create_local_vec_store():
    # Initialize Ollama embeddings
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")

    # Creating Local Vector Store
    vector_store = Chroma(
        embedding_function=embeddings
    )
    return vector_store

# ---------- Adding Documents Vector Store Function ----------
def add_docs_to_store(vector_store, docs):
    documents = []
    for doc in docs:
        documents.append(Document(
            page_content=doc
        ))
    vector_store.add_documents(documents=documents)

# ---------- Query Search Function ----------
def query_search(vector_store, query, k):
    results = vector_store.similarity_search(
        query, k
    )
    results = [result.page_content for result in results]
    return results