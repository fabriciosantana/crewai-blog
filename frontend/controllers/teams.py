import requests
from utils import get_backend_url

def list():
    response = requests.get(f"{get_backend_url()}/teams/list")
    if response.status_code == 200:
        return response.json()
    else:
        return []

def add(team_name: str):
    print("Adicionando time")
    response = requests.post(f"{get_backend_url()}/teams/create_team", json={"name": team_name})
    print(f"Response: {response.text}")
    if response.status_code == 200:
        return response.json()
    else:
        return []
    
def delete(team_id):
    response = requests.delete(f"{get_backend_url()}/teams/delete/{team_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return []

def update(team):
    response = requests.put(f"{get_backend_url()}/teams/update/{team['_id']}", json={"name": team["name"]})

    if response.status_code == 200:
        return response.json()
    else:
        return []

def fetch_agents(team_id: str):
    response = requests.get(f"{get_backend_url()}/teams/{team_id}/agents/list")
    if response.status_code == 200:
        return response.json()
    else:
        #st.error(f"Erro ao buscar times: {response.status_code} - {response.text}")
        return []

def add_agent(team_id: str, agent_data):
    response = requests.post(f"{get_backend_url()}/teams/{team_id}/add_agent", json=agent_data)
    if response.status_code == 200:
        return response.json()
    else:
        return []

def delete_agent(agent_id):
    response = requests.delete(f"{get_backend_url()}/teams/agents/delete/{agent_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return []

def get_tasks(team_id: str, agent_id: str):
    response = requests.get(f"{get_backend_url()}/teams/{team_id}/agents/{agent_id}/tasks/list")
    print(f"Response: {response.text}")
    if response.status_code == 200:
        return response.json()
    else:
        #st.error(f"Erro ao buscar times: {response.status_code} - {response.text}")
        return []

def add_task(team_id: str, agent_id: str, task_data):
    response = requests.post(f"{get_backend_url()}/teams/{team_id}/agents/{agent_id}/tasks/add", json=task_data)
    if response.status_code == 200:
        return response.json()
    else:
        return []
