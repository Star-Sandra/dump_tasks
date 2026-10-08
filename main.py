from fastapi import FastAPI

app = FastAPI(title="Dump Tasks API")


@app.get("/system-status")
def system_status():
    return {"status": "ok"}