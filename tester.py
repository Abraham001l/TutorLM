from vectordb_pipeline import *
from weaviate.classes.config import Configure

client = connect_to_client()
collec = get_collection(client, "db1")
# data = [{'data':'this is how you do matrix multiplcation'}, {'data':'to take the dot product of two matrices is done by'}]
# # add_data(collec, data, ['data'])
chunks = query_data(collec, 'matrix multiplication', 10)
# print_data(chunks)

# try:
#   def get_embedding(text, model):
#       embedding = client.embeddings.create(input=[text], model=model).data[0].embedding
#       return embedding

#   print(get_embedding('matrix multiplication', 'Snowflake/snowflake-arctic-embed-l-v2.0'))
# except:
#    close_client(client)

try:
  for obj in chunks.objects:
      print(len(obj.vector['default']))
      print(obj.properties['data'])
except:
  close_client(client)
close_client(client)