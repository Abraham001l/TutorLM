from llm_pipeline import llm_model, make_ollama_model

model = make_ollama_model('123456')

print(model.query_model("Hi! I'm Bob.", "Abraham is a good guy"))

print(model.query_model("what's my name and is abraham a good guy", ""))