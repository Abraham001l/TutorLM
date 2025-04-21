from rag_pipeline import rag
from vectordb_pipeline import close_client

ragger = rag()
ragger.question_answer("how does photosynthesis work")
close_client(ragger.weaviate_client)