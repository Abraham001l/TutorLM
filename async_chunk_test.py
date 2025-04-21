import asyncio
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain_core.embeddings import Embeddings
from typing import List
from sentence_transformers import SentenceTransformer

class SentenceTransformerEmbeddings(Embeddings):
    """Wrapper for SentenceTransformers to work with LangChain's SemanticChunker"""
    def __init__(self, model):
        self.model = model
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings = self.model.encode(texts, convert_to_tensor=False)
        return embeddings.tolist()
    
    def embed_query(self, text: str) -> List[float]:
        embedding = self.model.encode(text, convert_to_tensor=False)
        return embedding.tolist()

async def async_chunk_documents(documents):
    """
    Asynchronously chunks a list of documents using SemanticChunker.

    Args:
        documents (list[Document]): A list of Langchain Document objects.

    Returns:
        list[Document]: A list of chunked Langchain Document objects.
    """
    text_splitter = SemanticChunker(
        SentenceTransformerEmbeddings(SentenceTransformer('Snowflake/snowflake-arctic-embed-l-v2.0')), 
    )
    
    # Use `abatch` for concurrent processing of multiple documents
    chunks = await text_splitter.abatch(documents)
    
    # Alternatively, use `ainvoke` for a single document
    # chunks = await asyncio.gather(*[text_splitter.ainvoke(doc) for doc in documents])

    return chunks

async def main():
    # Example Usage
    documents = [
        Document(page_content="This is the first document. It has multiple sentences."),
        Document(page_content="This is the second document. It also has several sentences."),
    ]

    chunked_documents = await async_chunk_documents(documents)

    # Print the chunked documents
    for chunks in chunked_documents:
      for chunk in chunks:
        print(chunk)

if __name__ == "__main__":
    asyncio.run(main())