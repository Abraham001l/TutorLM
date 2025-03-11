from db_pipeline import *
from chunker_pipeline import *
import json

client = connect_to_client()
db = get_collection(client, 'db1')
text = """A cool fact is that 70% of cells are made of water. 
When a force applied to a string is passed through a pulley, the force on the other end is halved. 
Meanwhile, in astronomy, black holes are regions of spacetime where gravity is so strong that nothing can escape from them."""
# new_data = [{'title':'white cells','text':'white cells protect the body'}]
# keys = ['title', 'text']
# add_data(db, new_data, keys)
chunks = chunk(text)
chunks_to_db(db, chunks)
data = query_data(db,"forces", 2)
print_data(data)
close_client(client)