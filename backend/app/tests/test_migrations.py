from sqlalchemy import text
from app.db.session import SessionLocal


def test_articles_table_exists():
    db = SessionLocal()
    try:
        # PostgreSQL: to_regclass retourne NULL si la table n'existe pas
        res = db.execute(text("SELECT to_regclass('public.articles');")).scalar_one()
        assert res == "articles"
    finally:
        db.close()
