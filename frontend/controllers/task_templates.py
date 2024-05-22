import requests
from utils import get_backend_url

def list():
    response = requests.get(f"{get_backend_url()}/task_templates/list")
    if response.status_code == 200:
        return response.json()
    else:
        return []