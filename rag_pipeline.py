from llm_pipeline import llm_model, make_ollama_model
from vectordb_pipeline import connect_to_client, load_env_vars
from sentence_transformers import SentenceTransformer
import numpy as np
import math

class rag():
    def __init__(self):
        self.weaviate_client = connect_to_client()
        self.llm = make_ollama_model('123456', self.weaviate_client)
    
    def question_answer(self, question):
        # Compress question to topic
        query = self.question_to_topic(question)

        # Query local llm vector DB
        chunks = self.llm.query_qd_vdb(query)

        # Evaluate chunk results
        



    def question_to_topic(self, question):
        return 'matrix multiplication'
    
    def evaluate_results(self, query, chunks):
        
    