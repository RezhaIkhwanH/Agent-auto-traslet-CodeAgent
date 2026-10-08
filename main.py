from langchain_core.messages import HumanMessage
from dataclasses import Field
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from agent import voice_translate_agent


class CustomAgentInput(BaseModel):
    messages: list[dict] 
    
app = FastAPI(
    title="Voice Translation Agent",
    description="API agent untuk menerjemahkan transkrip voice ke Bahasa Indonesia.",
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
    voice_translate_agent,
    path="/voice-translate",
    playground_type="default",
    input_type=CustomAgentInput
)

@app.get("/health",tags=["health"])
async def health():
    return {"status": "ok"}
