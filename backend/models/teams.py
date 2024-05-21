from pydantic import BaseModel

class Team(BaseModel):
    name: str

class Agent(BaseModel):
    role: str
    goal: str
    context: str

class Activity(BaseModel):
    description: str
    expected_output: str
