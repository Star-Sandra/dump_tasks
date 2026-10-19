from fastapi import FastAPI

from app.routers import task_sources

app = FastAPI(title="Dump Tasks API")
app.include_router(task_sources.router)


@app.get("/system-status")
def system_status():
    return {"status": "ok"}
