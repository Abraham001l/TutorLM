from langchain_experimental.text_splitter import SemanticChunker
from langchain_ollama import OllamaEmbeddings
from vectordb_pipeline import add_data
from sentence_transformers import SentenceTransformer
from langchain_core.embeddings import Embeddings
from typing import List
import numpy as np

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

class chunker():
    def __init__(self, embedder):
        # Initializing embedder and semantic chunker
        self.embedder = embedder
        self.text_splitter = SemanticChunker(self.embedder)
    
    def semantic_chunk(self, docs):
        """
        Parameters:
        text (string): text which will be split into chunks

        Returns:
        docs (list<string>): A list of chunks(strings) which the text has been split into
        """

        # Split the text into semantically similar chunks
        docs = self.text_splitter.create_documents(docs)
        print(docs)
        chunks = [chunk.page_content for chunk in docs]
        return chunks

    def simple_chunk(self, docs):
        chunks = []
        for doc in docs:
            new_chunks = self.word_count_split(doc)
            chunks.extend(new_chunks)
        return chunks
    
    def word_count_split(self, text, chunk_size=300):
        words = text.split()
        return [
            ' '.join(words[i:i+chunk_size])
            for i in range(0, len(words), chunk_size)
        ]

# # ---------- Chunker Function ----------
# def chunk(text, embeddings):
#     """
#     Parameters:
#     text (string): text which will be split into chunks
#     embeddings (embeddings function): embedding function like say OllamaEmbeddings()

#     Returns:
#     docs (list<string>): A list of chunks(strings) which the text has been split into
#     """

#     # Create the SemanticChunker with Ollama embeddings
#     text_splitter = SemanticChunker(embeddings=embeddings)

#     # Split the text into semantically similar chunks
#     docs = text_splitter.create_documents([text])
#     docs = [doc.page_content for doc in docs]
#     return docs

# # ---------- Adding Chunks To DB ----------
# def chunks_to_db(db, chunks):
#     chunks = [{'data':chunk} for chunk in chunks]
#     add_data(db, chunks, ['content'])


# c_chunker = chunker(SentenceTransformerEmbeddings(SentenceTransformer('Snowflake/snowflake-arctic-embed-l-v2.0')))

# text1 = "to perform photosynthesis plants use the leafs to absorb nutrients. When finding the energy of a ball as it falls you simply convert the graviational potential energy to kinetic. Additionally this relates to Ug which is gravitational potential energy."
# text2 = """In the vast ecosystems of tropical rainforests, mutualistic relationships between fungi and plant roots—known as mycorrhizae—play a crucial role in nutrient exchange. These underground networks allow plants to access phosphorus and nitrogen more efficiently, ultimately enhancing their growth and resilience. Interestingly, recent studies show that these symbiotic fungi can even communicate stress signals between trees.
# Now, if we consider a system of linear equations representing the flow of resources between interconnected species, we can represent this interaction using a matrix A and a vector x, where Ax = b encodes the nutrient flow constraints across the network. To determine if this system has a unique solution, we check if A is invertible—meaning its determinant is non-zero. And let’s not forget eigenvalues: they tell us about the stability of the system, just like feedback loops in biological systems."""
# print(c_chunker.chunk([text1,text2]))
