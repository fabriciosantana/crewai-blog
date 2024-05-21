from pydantic import BaseModel

class BlogRequest(BaseModel):
    topic: str

class BlogResponse(BaseModel):
    content: str
