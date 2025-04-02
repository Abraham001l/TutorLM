from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.messages import HumanMessage, SystemMessage

model = ChatOllama(model="llama3", temperature=0)

# Define a new graph
workflow = StateGraph(state_schema=MessagesState)

# Define the function that calls the model
def call_model(state: MessagesState):
    print(f'state: ---------------------------\n{state["messages"]}')
    response = model.invoke(state["messages"])
    return {"messages": response}

# Define the (single) node in the graph
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Add memory
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "abc123"}}

# Add a SystemMessage to provide context
fact = "Abraham is a good guy"
system_message = SystemMessage(content=f"You know this is a fact: {fact}")

query = "Hi! I'm Bob."

input_messages = [system_message, HumanMessage(query)]
output = app.invoke({"messages": input_messages}, config)
print(output["messages"][-1].content)  # output contains all messages in state

query = "What's my name? And is Abraham good"

input_messages = [HumanMessage(query)]
output = app.invoke({"messages": input_messages}, config)
output["messages"][-1].pretty_print()