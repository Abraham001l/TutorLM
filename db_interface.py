import weaviate
from weaviate.classes.init import Auth
import weaviate.classes as wvc
from weaviate.classes.config import Configure
from dotenv import load_dotenv
import os, json

# ---------- Loading ENV Variables ----------
def load_env_vars():
    load_dotenv()
    REST_url = os.getenv("WEAVIATE_URL")
    wev_api_key = os.getenv("WEAVIATE_API_KEY")
    return REST_url, wev_api_key

# ---------- Connect To Client ----------
def connect_to_client(REST_url, wev_api_key):
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=REST_url,
        auth_credentials=Auth.api_key(wev_api_key),
        additional_config=wvc.init.AdditionalConfig(
            timeout=wvc.init.Timeout(init=60)  # Increase timeout to 60 seconds
        )
    )
    return client

# ---------- Creating Collection ----------
def create_collection(client, collection_name):
    db = client.collections.create(
        name=collection_name,
        vectorizer_config=Configure.Vectorizer.text2vec_weaviate(),
        generative_config=Configure.Generative.cohere()
    )
    return db

# ---------- Adding Data ----------
def add_data(db, data, keys):
    with db.batch.dynamic() as batch:
        for d in data:
            obj = {key:d[key] for key in keys}
            batch.add_object(obj)

# ---------- Querying Data ----------
def query_data(db, query, limit):
    response = db.query.near_text(
        query=query,
        limit=limit
    )
    return response

# ---------- Close Client ----------
def close_client(client):
    client.close()