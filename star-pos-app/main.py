import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from app.routers import catalog, payments, products, sales, users

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Star POS API",
    description="A fast, lightweight POS backend for Star Supermarket: cashiers, "
                 "product catalog inventory, shopping cart checkouts, and payment tracking.",
    version="1.0.0",
    lifespan=lifespan,
)

ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", "").split(",")
    if origin.strip()
] or ["http://localhost:3000", "http://127.0.0.1:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "OPTIONS", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(users.router)
app.include_router(catalog.router)
app.include_router(products.router)
app.include_router(sales.router)
app.include_router(payments.router)


@app.get("/", tags=["System Status"])
def read_root():
    return {
        "status": "online",
        "service": "Star POS Core Framework",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
