import requests
from typing import List
from utils import get_backend_url

def add(assignment: dict):
    response = requests.post(f"{get_backend_url()}/assignments/add", json=assignment)
    if response.status_code == 200:
        return response.json()
    else:
        return []
    
def list():
    response = requests.get(f"{get_backend_url()}/assignments/list")
    if response.status_code == 200:
        return response.json()
    else:
        return []
    
def delete_many(assignment_ids: List[str]):
    response = requests.delete(f"{get_backend_url()}/assignments/delete", json={"assignment_ids": assignment_ids})
    if response.status_code == 200:
        return response.json()
    else:
        return []