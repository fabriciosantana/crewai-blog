import os
from typing import List
from crewai import Agent, Task, Crew
from utils import get_openai_api_key, get_mongo_db
from datetime import datetime
from bson.objectid import ObjectId

def execute(assignment: dict):
    
    openai_api_key = get_openai_api_key()
    os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'

    agent_list = []
    task_list = []

    if assignment:
        for agent in assignment["assigned_to"]["agents"]:
            agent_list.append( Agent(
                role = agent["role"],
                goal = agent["goal"],
                backstory = agent["backstory"],
                allow_delegation=False,
                verbose=True))
            for task in agent["tasks"]:
                task_list.append(Task(
                    description = task["description"],
                    expected_output = task["expected_output"],
                    agent=agent))

        crew = Crew(
        agents=agent_list,
        tasks=task_list,
        verbose=2)

        result = crew.kickoff(inputs={"topic": assignment["title"]})
        #result = "Teste. Crew está desligado"

        try:

             # Conectar ao MongoDB e armazenar o resultado
            db = get_mongo_db()
            assignments_collection = db["assignments"]  # Nome da coleção
            post = {
                "content": result,
                "status": "Concluído",
                "finished_at": datetime.now() 
            }
            assignments_collection.update_one({"_id": ObjectId(assignment["_id"])}, {"$set": post})

            print("Atualizaou") 
        except Exception as e:
            print(str(e))
    else:
        print("deu ruim")
        result = []

    return result




