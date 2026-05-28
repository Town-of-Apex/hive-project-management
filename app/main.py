"""
app/main.py

FastAPI application factory.
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from app.core.config import settings
from app.core.database import init_db
from app.core.exceptions import AppException, app_exception_handler, http_exception_handler

from app.api.routes import users as user_router
from app.api.routes import db_status as db_status_router
from app.api.routes import comments as comment_router
from app.api.routes import departments as department_router
from app.api.routes import goals as goal_router
from app.api.routes import project_members as project_member_router
from app.api.routes import projects as project_router
from app.api.routes import status_updates as status_update_router
from app.api.routes import tasks as task_router
from app.api.routes import teams as team_router
from app.api.routes import auth as auth_router

app = FastAPI(
    root_path=settings.BASE_PATH,
    title="Hive Project Management",
    description="Internal project management platform for the Town of Apex.",
    version="0.6.0",
)

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(db_status_router.router)
app.include_router(comment_router.router)
app.include_router(department_router.router)
app.include_router(goal_router.router)
app.include_router(project_member_router.router)
app.include_router(project_router.router)
app.include_router(status_update_router.router)
app.include_router(task_router.router)
app.include_router(team_router.router)


@app.get("/app_metadata.json", include_in_schema=False)
async def get_metadata():
    return FileResponse("app_metadata.json")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
