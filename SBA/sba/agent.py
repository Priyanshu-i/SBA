from pydantic import BaseModel
from typing import Optional, List, Dict, Callable

class Agent(BaseModel):
    name: str = "Agent"
    instructions: str = "You are a helpful Agent"
    tools: List[Callable] = []

class Response(BaseModel):
    agent: Optional[Agent]
    messages: List[Dict]