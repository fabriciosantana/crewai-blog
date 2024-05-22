from fastapi import FastAPI
from routers import blog, teams, agent_templates

app = FastAPI()

app.include_router(blog.router, prefix="/blog", tags=["blog"])
app.include_router(teams.router, prefix="/teams", tags=["teams"])
app.include_router(agent_templates.router, prefix="/agent_templates", tags=["agent_templates"])

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0')
