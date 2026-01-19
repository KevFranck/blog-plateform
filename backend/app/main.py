from fastapi import FastAPI

from app.routers.articles import router as articles_router


app= FastAPI(title = "Blog Platform API", version = "0.1.0")

app.include_router(articles_router)
@app.get("/health")
def health():
    return {"status": "ok"}
