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
        agent_templates_collection = db["agent_templates"]
        agent_templates = list(agent_templates_collection.find({}))

        for agent_template in agent_templates:
            agent_template['_id'] = str(agent_template['_id']) 

        return agent_templates
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
