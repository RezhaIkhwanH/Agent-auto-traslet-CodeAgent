from langchain_core.messages import HumanMessage
from dataclasses import Field
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from agent import agent_MOM 


class CustomAgentInput(BaseModel):
    messages: list[dict] 
    
app = FastAPI(
    title="Agent notetaker MOM",
    description="Agent notetaker MOM",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

add_routes(
    app, 
    agent_MOM, 
    path="/agent_MOM",
    playground_type="default",
    input_type=CustomAgentInput
)

@app.get("/health",tags=["health"])
async def health():
    return {"status": "ok"}
