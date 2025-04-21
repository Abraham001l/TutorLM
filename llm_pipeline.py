from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.messages import HumanMessage, SystemMessage
from vectordb_pipeline import create_collection, add_data, query_data, get_collection

class llm_model():
    def __init__(self, model, config_key, weaviate_client):
        self.next_doc_id = 0
        self.model = model

        # Defining the State Graph
        self.workflow = StateGraph(state_schema=MessagesState)

        # Define the (single) node in the graph
        self.workflow.add_edge(START, "model")
        self.workflow.add_node("model", self.call_model)

        # Add memory
        memory = MemorySaver()
        self.model_instance = self.workflow.compile(checkpointer=memory)

        # Config Key for memory
        self.config = {"configurable":{"thread_id":config_key}}

        # Initializing local vector DB
        self.init_vdb_client(weaviate_client)
        self.create_qd_vdb()

    # ---------- Call Model Function For Workflow ----------
    def call_model(self, state: MessagesState):
        response = self.model.invoke(state['messages'])
        return {"messages": response}
    
    # ---------- Query Model Function For Application Use ----------
    def query_model(self, query, context):
        # Setting Up Message
        system_message = SystemMessage(content=context)
        human_message = HumanMessage(content=query)
        input_messages = [system_message, human_message]

        # Invoking model_instance
        output = self.model_instance.invoke({"messages":input_messages}, self.config)
        return output["messages"][-1].content
    
    # ---------- Compress Previouse Context ----------
    # TODO

    # ---------- Initialize Vector DB Client ----------
    def init_vdb_client(self, client):
        """
        Parameters:
        client(WeaviateClient): client connected to weaviate
        """
        self.client = client
    
    # ---------- Create Query Data Collection Vector DB ----------
    def create_qd_vdb(self):
        """
        Creates query data vector data base
        """
        try:
            self.query_data_vdb = create_collection(self.client,'query_data_vdb')
        except:
            self.query_data_vdb = get_collection(self.client,'query_data_vdb')
    
    # ---------- Add Data to Query Data ----------
    def add_data_to_qd_vdb(self, docs):
        """
        Parameters:
        docs (list<string>): list of data you want to add to query data vector data base
        """
        data = [{f'data':docs[i]} for i in range(len(docs))]
        keys = ['data']
        add_data(self.query_data_vdb, data, keys)
    
    # ---------- Query the Query Data Vector DB ----------
    def query_qd_vdb(self, query):
        """
        Parameters:
        query (string): query being queried

        Returns:
        data (list<string>): data gathered from query
        """
        response = query_data(self.query_data_vdb, query, 4)
        return response
    
    # ---------- Prepare Data for System Message ----------
    def prepare_info(self, docs):
        """
        Parameters:
        docs (list<string>): docs being fed to llm as info on topic

        Returns:
        sys_msg (string): system message ready to be fed to llm
        """
        sys_msg = ""
        sys_msg += "This is info that may help you answer the question:\n"
        for d in docs:
            sys_msg += f"Info 1: "+d+"\n"
        return sys_msg
    
    # ---------- Check Relevancy of Queried Data ----------
    # TODO


def make_ollama_model(config_key, weaviate_client):
    """
    Prameters:
    config_key (string): config key to allow model to keep memory
    weaviate_client (WeaviateClient): weaviate client

    Returns:
    llm_model (llm_model): ollama llm_model
    """
    model = ChatOllama(model="llama3", temperature=0)
    ollama_llm_model  = llm_model(model, config_key, weaviate_client)
    return ollama_llm_model