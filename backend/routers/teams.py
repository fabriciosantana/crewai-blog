from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from bson.objectid import ObjectId
import utils
from models.teams import Team, Agent, Activity

router = APIRouter()

@router.get("/list")
def get_teams():
    try:
        db = utils.get_mongo_db()
        teams_collection = db["teams"]
        teams = list(teams_collection.find({}, {"_id": 1, "name": 1}))

        for team in teams:
            team['_id'] = str(team['_id'])

        return teams
        #print("Recuparando os times")
        #for team in teams:
        #    print(team)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/teams/{team_id}")
def update_team(team_id: str, team: Team):
    try:
        db = utils.get_mongo_db()
        teams_collection = db["teams"]
        result = teams_collection.update_one({"_id": ObjectId(team_id)}, {"$set": team.dict()})
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Team not found")
        return {"message": "Team updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/teams/{team_id}")
def delete_team(team_id: str):
    try:
        db = utils.get_mongo_db()
        teams_collection = db["teams"]
        result = teams_collection.delete_one({"_id": ObjectId(team_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Team not found")
        return {"message": "Team deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create_team")
def create_team(team: Team):
    try:
        db = utils.get_mongo_db()
        teams_collection = db["teams"]
        result = teams_collection.insert_one(team.dict())
        return {"message": "Time criado com sucesso", "team_id": f"{result.inserted_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{team_id}/add_agent")
def add_agent(team_id: str, agent: Agent):
    try:
        db = utils.get_mongo_db()

        teams_collection = db["teams"]

        print("teste")
        agent_data = agent.model_dump()

        print(agent_data)

        agent_data["_id"] = str(ObjectId())

        result = teams_collection.update_one(
            {"_id": ObjectId(team_id)},
            {"$push": {"agents": agent_data}}
        )

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Team not found")
        
        updated_team = teams_collection.find_one({"_id": ObjectId(team_id)})
        last_agent = updated_team["agents"][-1]

        return {"message": "Agente adicionado com sucesso", "agent_id": f"{last_agent['_id']}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{team_id}/{agent_id}/add_activity")
def add_activity(team_id: str, agent_id: str, activity: Activity):
    try:
        db = utils.get_mongo_db()
        teams_collection = db["teams"]

        activity_data = activity.model_dump();

        activity_data["_id"] = str(ObjectId())

        result = teams_collection.update_one(
            {"agents._id": agent_id},
            {"$push": {"agents.$.activities": activity_data}}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Agent not found in any team")
        return {"message": "Activity added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
