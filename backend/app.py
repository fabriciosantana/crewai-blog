from fastapi import FastAPI
from routers import ping, blog, teams, agent_templates, task_templates, assignment

app = FastAPI()

app.include_router(ping.router, prefix="/health", tags=["health"])
app.include_router(blog.router, prefix="/blog", tags=["blog"])
app.include_router(teams.router, prefix="/teams", tags=["teams"])
app.include_router(agent_templates.router, prefix="/agent_templates", tags=["agent_templates"])
app.include_router(task_templates.router, prefix="/task_templates", tags=["task_templates"])
app.include_router(assignment.router, prefix="/assignments", tags=["task_templates"])

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0')
