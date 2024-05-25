from fastapi import APIRouter, HTTPException
from typing import List

from pymongo import DESCENDING
import utils
from bson.objectid import ObjectId
from ai import crewai_wrapper

router = APIRouter()

@router.post("/add")
def add(assignment: dict):
    try:
        db = utils.get_mongo_db()
        assignments_collection = db["assignments"]
        result = assignments_collection.insert_one(assignment)
        
        crewai_wrapper.execute(assignment)

        return {"message": "Atribuição criado com sucesso", "assignment_id": f"{result.inserted_id}"}
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list")
def get_all():
    try:
        db = utils.get_mongo_db()
        assignments_collection = db["assignments"]
        assignments = list(assignments_collection.find({}).sort("created_at", DESCENDING))
        for assignment in assignments:
            assignment['_id'] = str(assignment['_id'])

        return assignments
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete")
def delete_many(assignment_ids: dict):
    try:
        db = utils.get_mongo_db()
        assignments_collection = db["assignments"]
        # Converte os IDs da string para ObjectId
        object_ids = [ObjectId(assignment_id) for assignment_id in assignment_ids["assignment_ids"]]
        # Deleta os times com os IDs fornecidos
        result = assignments_collection.delete_many({"_id": {"$in": object_ids}})

        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="No assignments found to delete")
        
        return {"message": f"{result.deleted_count} assignments deleted successfully"}
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))