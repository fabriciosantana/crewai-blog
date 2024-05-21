from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from blog import generate_blog_content
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import utils

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

@app.get("/get_posts")
def get_posts():
    try:
        db = utils.get_mongo_db()
        collection = db["blog_posts"]
        posts = list(collection.find({}, {"_id": 0}))  # Excluir o campo _id da resposta
        return posts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0')
