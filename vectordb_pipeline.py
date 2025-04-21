import weaviate
from weaviate.classes.init import Auth
import weaviate.classes as wvc
from weaviate.classes.config import Configure
from dotenv import load_dotenv
import os, json
from weaviate.classes.query import MetadataQuery

# ---------- Loading ENV Variables ----------
def load_env_vars():
    load_dotenv()
    REST_url = os.getenv("WEAVIATE_URL")
    wev_api_key = os.getenv("WEAVIATE_API_KEY")
    return REST_url, wev_api_key

# ---------- Connect To Client ----------
def connect_to_client():
    """
    Returns:
    client (WeaviateClient): weaviate client
    """
    REST_url, wev_api_key = load_env_vars()
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=REST_url,
        auth_credentials=Auth.api_key(wev_api_key),
        additional_config=wvc.init.AdditionalConfig(
            timeout=wvc.init.Timeout(init=100)  # Increase timeout to 60 seconds
        )
    )
    return client

# ---------- Creating Collection ----------
def create_collection(client, collection_name):
    """
    Parameters:
    client (WeaviateClient): weaviate client
    collection_name (string): name of collection being created
    
    Returns:
    db (Collection): weaviate vector data base
    """
    db = client.collections.create(
        name=collection_name,
        vectorizer_config=Configure.Vectorizer.text2vec_weaviate(
            model="Snowflake/snowflake-arctic-embed-l-v2.0"
        ),
        generative_config=Configure.Generative.cohere()
    )
    return db

# ---------- Get Collection ----------
def get_collection(client, collection_name):
    """
    Parameters:
    client (WeaviateClient): weaviate client

    Returns:
    db (Collection): weaviate vector data base
    """
    return client.collections.get(collection_name)

# ---------- Adding Data ----------
def add_data(vdb, data, keys):
    """
    Parameters:
    vdb (Collection): weaivate vector data base
    data (list<dict>): dictionary of docs in this format: [{"data":"actual data1"},...,{"data":"actual data2"}]
    keys (list<string>): list of keys for key-value pairs which is in each data entry in data *all data needs to have the same format*
    """
    with vdb.batch.dynamic() as batch:
        # looping throw data to add to batch
        for d in data:
            obj = {key:d[key] for key in keys}
            batch.add_object(obj)

# ---------- Querying Data ----------
def query_data(vdb, query, limit):
    """
    Parameter:
    vdb (Collection): weaviate vector data base
    query (string): the query
    limit (int): how many docs to query

    Returns:
    response (objects): list of objects in format: [{"data":"actual data1"},...,{"data":"actual data2"}]
    """
    response = vdb.query.near_text(
        query=query,
        limit=limit,
        include_vector=True,
    )
    return response

# ---------- Print Data ----------
def print_data(data):
    """
    Parameter:
    data (response): response from weaviate query

    Prints:
    data in objects in response
    """
    for obj in data.objects:
        print(obj.properties['data'])
        print(json.dumps(obj.properties, indent=2))

# ---------- Close Client ----------
def close_client(client):
    client.close()