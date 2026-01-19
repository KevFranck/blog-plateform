import uuid
from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, Field

# 1. what client send to server
class ArticleCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    content: str = Field(min_length=10)
    status: Literal['draft', 'published'] = 'draft'


# 2. what clinet send to server to update an article
class ArticleUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=200)
    content: Optional[str] = Field(default=None, min_length=10)
    status: Optional[Literal['draft', 'published']] = None


# 3. what API send to client
class ArticleOut(BaseModel):
    id: uuid.UUID
    title: str
    content: str
    status: str
    image_url: Optional[str]
    created_at: datetime
    updated_at: datetime

# Important: Pydantic models convert SQLAlchemy objects to JSON response
    model_config = {"from_attributes": True}
