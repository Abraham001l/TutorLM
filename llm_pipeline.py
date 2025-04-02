from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.messages import HumanMessage, SystemMessage

class llm_model():
    def __init__(self, model, config_key):
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

def make_ollama_model(config_key):
    model = ChatOllama(model="llama3", temperature=0)
    return llm_model(model,config_key)