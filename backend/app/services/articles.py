from datetime import datetime, timezone

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.article import Article
from app.schemas.article import ArticleCreate, ArticleUpdate


class ArticleService:
    """
    Service = logic, independent of HTTP.
    we receive a BD session, we do the operations,
    and we return the objects (Article).
    """

    @staticmethod
    def create(db: Session, data: ArticleCreate) -> Article:
        # 1 verify unique title
        exists = db.execute(select(Article).where(Article.title == data.title)).scalar_one_or_none()
        if exists:
            raise ValueError("Article with this title already exists.")

        # 2 create the object SQLAlchemy
        article = Article(
            title=data.title,
            content=data.content,
            status=data.status,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )

        # 3 save to DB
        db.add(article)
        db.commit()
        db.refresh(article)  # to get the generated ID

        return article

    @staticmethod
    def get(db: Session, article_id) -> Article | None:
        return db.get(Article, article_id)

    @staticmethod
    def list(db: Session, *, limit: int = 20, offset: int = 0) -> list[Article]:
        stmt = select(Article).order_by(Article.created_at.desc()).limit(limit).offset(offset)
        return list(db.execute(stmt).scalars().all())

    @staticmethod
    def update(db: Session, article: Article, data: ArticleUpdate) -> Article:
        #if data.title is being updated, check uniqueness
        if data.title and data.title != article.title:
            exists = db.execute(select(Article).where(Article.title == data.title)).scalar_one_or_none()
            if exists:
                raise ValueError("Article with this title already exists.")
            article.title = data.title

        if data.content is not None:
            article.content = data.content

        if data.status is not None:
            article.status = data.status

        article.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(article)
        return article

    @staticmethod
    def delete(db: Session, article: Article) -> None:
        db.delete(article)
        db.commit()
