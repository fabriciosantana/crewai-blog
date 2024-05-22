from pydantic import BaseModel

class Team(BaseModel):
    name: str

class Agent(BaseModel):
    role: str
    goal: str
    backstory: str

class Task(BaseModel):
    title: str
    description: str
    expected_output: str
