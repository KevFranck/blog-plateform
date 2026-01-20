from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers.articles import router as articles_router


app= FastAPI(title = "Blog Platform API", version = "0.1.0")

app.mount("/media", StaticFiles(directory="media"), name="media")

app.include_router(articles_router)
@app.get("/health")
def health():
    return {"status": "ok"}
