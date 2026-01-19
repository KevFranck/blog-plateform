import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
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
