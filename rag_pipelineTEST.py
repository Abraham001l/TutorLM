from rag_pipeline import rag
from vectordb_pipeline import close_client

ragger = rag()
ragger.question_answer_rag("""Endothelium calls macrophages for destruction""")
print('-------------------------------------------------------------------------')
# ragger.question_answer_raw("""Endothelium calls macrophages for destruction""")
close_client(ragger.weaviate_client)

