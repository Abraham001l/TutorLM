from llm_pipeline import llm_model, make_ollama_model
print(-1)
from vectordb_pipeline import connect_to_client, load_env_vars, get_collection, query_data
print(-2)
from sentence_transformers import SentenceTransformer
print(-3)
import numpy as np
print(-4)
import math
print(-5)
from scraper_pipeline import web_query_to_data
print(-6)
import asyncio
print(-7)
from chunker_pipeline import chunker, SentenceTransformerEmbeddings
print(-8)


class rag():
    def __init__(self):
        self.weaviate_client = connect_to_client()
        print('1')
        self.llm = make_ollama_model('123456', self.weaviate_client)
        print('2')
        self.embedding_model = SentenceTransformer('Snowflake/snowflake-arctic-embed-l-v2.0')
        print('3')
        self.chunker = chunker(SentenceTransformerEmbeddings(self.embedding_model))
        print('4')
        self.main_vdb = get_collection(self.weaviate_client, 'tutorlm_main')
    
    def question_answer_rag(self, question):
        # Compress question to topic
        query, keywords = self.question_to_topic(question)
        print('5')

        # Query local llm vector DB
        chunks = self.llm.query_qd_vdb(query)
        print('6')

        # Evaluate chunk results
        good_results = self.evaluate_results(query, chunks)
        print('7')

        if good_results:
            # Prepare LLM context
            docs = [chunk.properties['data'] for chunk in chunks.objects]
            context = self.llm.prepare_info(docs)
            print('8g')

            # Feed question and context to llm
            llm_response = self.llm.query_model_memory(question, context)
            print(llm_response)
            print('9g')
        else:
            # Vector db process
            vdb_chunks = [obj.properties['data'] for obj in (query_data(self.main_vdb, query, 4)).objects]
            self.llm.add_data_to_qd_vdb(vdb_chunks)
            print('8o')

            # Scraper process
            web_content = asyncio.run(web_query_to_data(query, keywords, 1))
            web_chunks = self.chunker.simple_chunk(web_content)
            self.llm.add_data_to_qd_vdb(web_chunks)

            print('9o')

            # Query local llm vector DB
            chunks = self.llm.query_qd_vdb(query)

            print('10o')

            # Prepare LLM context
            docs = [chunk.properties['data'] for chunk in chunks.objects]
            context = self.llm.prepare_info(docs)

            print('11o')

            # Feed question and context to llm
            llm_response = self.llm.query_model_memory(question, context)
            print('12o')
            print(llm_response)

    # ---------- Raw Model Usage ----------
    def question_answer_raw(self, question):
        llm_response = self.llm.query_model_raw(question)
        print(llm_response)

    # ---------- Graph Architecture Generator ----------
    # def words_to_graph(self):

        
    # ---------- Angle Calculator ----------
    def extract_text(self, chunks):
        data = []

    # ---------- Question to Optimized Query ----------
    def question_to_topic(self, question):
        keywords = []
        return question, keywords
    
    # ---------- Evaluate Quality of Vector DB Results ----------
    def evaluate_results(self, query, chunks):
        # Embed the query
        q_v = self.embedding_model.encode([query])

        # Initializing variables for average angle calculation
        avg_angle = 0
        i = 0

        # Calculate average angle
        for obj in chunks.objects:
            doc_v = obj.vector['default']
            avg_angle += self.calc_angle(q_v, doc_v)
            i += 1

        # In case of no chunks avaliable
        if (i == 0):
            return False
        avg_angle /= i

        return avg_angle < 60
        
    # ---------- Angle Calculator ----------
    def calc_angle(self, v1, v2):
        # Normalize the vecotr to unit length
        u_v1 = v1/np.linalg.norm(v1)
        u_v2 = v2/np.linalg.norm(v2)

        # Calculate the dot product of the unit vectors
        dot_product = np.dot(u_v1, u_v2)

        # Clip the dot product to ensure it's within the valid range
        clipped_dp = np.clip(dot_product, -1.0, 1.0)

        # Calculate the angle in radians
        angle_rad = np.arccos(clipped_dp)

        # Return angle in degrees
        return angle_rad*(180/(math.pi))
    

