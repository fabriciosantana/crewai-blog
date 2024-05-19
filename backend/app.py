from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from blog import generate_blog_content

app = FastAPI()

class BlogRequest(BaseModel):
    topic: str

class BlogResponse(BaseModel):
    content: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/generate_blog", response_model=BlogResponse)
def generate_blog(request: BlogRequest):
    topic = request.topic
    try:
        content = generate_blog_content(topic)
        return BlogResponse(content=content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0')
