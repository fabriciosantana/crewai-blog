from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from bson.objectid import ObjectId
import utils
from models.teams import Team, Agent, Task

from models.team_delete_request import TeamDeleteRequest

router = APIRouter()

@router.get("/list")
def get_teams():
    try:
        db = utils.get_mongo_db()
        teams_collection = db["teams"]
        teams = list(teams_collection.find({}))

        for team in teams:
            team['_id'] = str(team['_id'])

        return teams
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update")
def update_team(team: dict):
    try:
        db = utils.get_mongo_db()
        teams_collection = db["teams"]

        team_id = team.pop("_id")

        result = teams_collection.update_one({"_id": ObjectId(team_id)}, {"$set": team})

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Team not found")
        return {"message": "Team updated successfully"}
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update_many")  
def update_many(teams: List[dict]):
    try:
        print(teams)
        for team in teams:
            update_team(team)

    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete/{team_id}")
def delete(team_id: str):
    try:
        db = utils.get_mongo_db()
        teams_collection = db["teams"]
        result = teams_collection.delete_one({"_id": ObjectId(team_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Team not found")
        return {"message": "Team deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.delete("/delete")
def delete_many(request: TeamDeleteRequest):
    try:
        db = utils.get_mongo_db()
        teams_collection = db["teams"]

        print(request)
        # Converte os IDs da string para ObjectId
        object_ids = [ObjectId(team_id) for team_id in request.team_ids]
        print(object_ids)
        # Deleta os times com os IDs fornecidos
        result = teams_collection.delete_many({"_id": {"$in": object_ids}})

        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="No teams found to delete")
        
        return {"message": f"{result.deleted_count} teams deleted successfully"}
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create_team")
def create_team(team: Team):
    try:
        db = utils.get_mongo_db()
        teams_collection = db["teams"]
        result = teams_collection.insert_one(team.model_dump())
        return {"message": "Time criado com sucesso", "team_id": f"{result.inserted_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/add_many")
def add_many(teams: List[dict]):
    try:
        db = utils.get_mongo_db()
        teams_collection = db["teams"]

        result = teams_collection.insert_many(teams)
        
        return {"message": f"{len(result.inserted_ids)} times criados com sucesso", "team_ids": [str(id) for id in result.inserted_ids]}

    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{team_id}/add_agent")
def add_agent(team_id: str, agent: Agent):
    try:
        db = utils.get_mongo_db()

        teams_collection = db["teams"]

        agent_data = agent.model_dump()

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

@router.get("/{team_id}/agents/list")
def get_agents(team_id: str):
    try:
        db = utils.get_mongo_db()
        teams_collection = db["teams"]
        team = teams_collection.find_one({"_id": ObjectId(team_id)}, {"agents": 1, "_id": 0})
        
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")

        return team.get("agents", [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/agents/delete/{agent_id}", response_model=dict)
def delete_agent(agent_id: str):
    try:
        db = utils.get_mongo_db()
        teams_collection = db["teams"]
        
        result = teams_collection.update_one(
            {"agents._id": agent_id},
            {"$pull": {"agents": {"_id": agent_id}}}
        )

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Agent not found")

        return {"message": "Agente excluído com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{team_id}/agents/{agent_id}/tasks/add")
def add_tasks(team_id: str, agent_id: str, task: Task):
    try:
        db = utils.get_mongo_db()
        teams_collection = db["teams"]

        task_data = task.model_dump();

        task_data["_id"] = str(ObjectId())

        result = teams_collection.update_one(
            {"agents._id": agent_id},
            {"$push": {"agents.$.tasks": task_data}}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Agent not found in any team")
        return {"message": "Activity added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{team_id}/agents/{agent_id}/tasks/list")
def get_tasks(team_id: str, agent_id: str):
    try:
        db = utils.get_mongo_db()
        teams_collection = db["teams"]
        team = teams_collection.find_one({"_id": ObjectId(team_id)}, {"agents": 1, "_id": 0})

        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
        
         # Encontra o agente específico pelo ID
        agent = next((agent for agent in team.get("agents", []) if agent["_id"] == agent_id), None)
                
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")

        print(agent)
        print(agent.get("tasks"))

        return agent.get("tasks", [])
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
