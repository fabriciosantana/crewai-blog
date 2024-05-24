from typing import List
from pydantic import BaseModel

class TeamDeleteRequest(BaseModel):
    team_ids: List[str]