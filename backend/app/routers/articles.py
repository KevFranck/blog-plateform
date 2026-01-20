import os
import uuid
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.article import ArticleCreate, ArticleOut, ArticleUpdate
from app.services.articles import ArticleService

router = APIRouter(prefix="/articles", tags=["articles"])

@router.post("", response_model=ArticleOut, status_code=201)
def create_article(payload: ArticleCreate, db: Session = Depends(get_db)):
    try:
        article = ArticleService.create(db, payload)
        return article
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{article_id}", response_model=ArticleOut)
def get_article(article_id: uuid.UUID, db: Session = Depends(get_db)):
    article = ArticleService.get(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@router.get("", response_model=list[ArticleOut])
def list_articles(
    db: Session = Depends(get_db),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    articles = ArticleService.list(db, limit=limit, offset=offset)
    return articles

@router.patch("/{article_id}", response_model=ArticleOut)
def update_article(
    article_id: uuid.UUID,
    payload: ArticleUpdate,
    db: Session = Depends(get_db)
):
    article = ArticleService.get(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    try:
        updated_article = ArticleService.update(db, article, payload)
        return updated_article
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{article_id}", status_code=204)
def delete_article(article_id: uuid.UUID, db: Session = Depends(get_db)):
    article = ArticleService.get(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    ArticleService.delete(db, article)
    return None

@router.post("/{article_id}/image", status_code=200)
def upload_article_image(
    article_id: uuid.UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    upload an image and associate with the article
    """
    article = ArticleService.get(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")


    #verify the type file
    if file.content_type not in {"image/jpg", "image/png", "image/webp"}:
        raise HTTPException(status_code=400, detail="Unsupported image file")

    #determine extension
    ext ={
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp",
    }[file.content_type]

    #unique name
    filename = f"{uuid.uuid4()}{ext}"

    #disk path
    media_dir = Path("media/") / "articles"
    media_dir.mkdir(parents=True, exist_ok=True)
    file_path = media_dir / filename

    # write the file
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    #save the URL in the DB
    # article.image_url = f"/media/articles/{filename}"
    # ArticleService.update(db, article, date=type("tmp", (), {"title":None, "content":None, "status": None})())
    ArticleService.set_image_url(db, article, f"/media/articles/{filename}")

    return {"image_url":article.image_url}
