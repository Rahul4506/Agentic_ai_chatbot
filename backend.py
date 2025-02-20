from pydantic import BaseModel
from typing import List



# If i get request from front end and data types are not from following defined types then this will throw error
class RequestState(BaseModel):
    model_name : str
    model_provider : str
    system_prompt : str
    messages : List[str]
    allow_search : bool

#Step2: Setup AI Agent from FrontEnd Request
from fastapi import FastAPI
from ai_agent import get_response_from_ai_agent

ALLOWED_MODEL_NAMES=["llama3-70b-8192", "llama-3.1-8b-instant", "llama-3.3-70b-versatile", "gpt-4o-mini"]

app = FastAPI(title="LangGraph Multimodal AI Agent")

@app.post("/chat")
def chat_endpoint(request : RequestState):
    """
    API Endpoint to interact with the Chatbot using LangGraph and search tools.
    It dynamically selects the model specified in the request
    """
    
    if request.model_name not in ALLOWED_MODEL_NAMES:
        return {"error": "Invalid model name . Kindly select valid model"}
    
    llm_id = request.model_name
    query = request.messages
    allow_search = request.allow_search
    system_prompt = request.system_prompt
    provider = request.model_provider

    # Create AI Agent and get response from it! 
    response=get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider)
    return response

#Step3: Run app & Explore Swagger UI Docs
if __name__ == "__main__":
    import uvicorn
    # uvicorn.run(app, host="127.0.0.1", port=9999)
    # uvicorn backend:app --host 0.0.0.0 --port 10000
    uvicorn.run(app, host="0.0.0.0", port=10000)
