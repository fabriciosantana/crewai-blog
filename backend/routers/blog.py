from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from blog import generate_blog_content
import utils
from models.blog import BlogResponse, BlogRequest

router = APIRouter()

@router.post("/generate_blog", response_model=BlogResponse)
def generate_blog(request: BlogRequest):
    topic = request.topic
    try:
        content = generate_blog_content(topic)
        return BlogResponse(content=content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_posts")
def get_posts():
    try:
        db = utils.get_mongo_db()
        collection = db["blog_posts"]
        posts = list(collection.find({}, {"_id": 0}))  # Excluir o campo _id da resposta
        return posts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
