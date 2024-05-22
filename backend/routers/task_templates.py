from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from bson.objectid import ObjectId
import utils

router = APIRouter()

@router.get("/list")
def get_teams():
    try:
        db = utils.get_mongo_db()
        task_templates_collection = db["task_templates"]
        task_templates = list(task_templates_collection.find({}))

        for task_template in task_templates:
            task_template['_id'] = str(task_template['_id']) 

        return task_templates
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
