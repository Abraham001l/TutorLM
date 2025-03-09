from db_interface import *
import json

client = connect_to_client()
db = get_collection(client, 'db1')
new_data = [{'title':'white cells','text':'white cells protect the body'}]
keys = ['title', 'text']
# add_data(db, new_data, keys)
data = query_data(db,"immune system", 2)
print_data(data)
close_client(client)