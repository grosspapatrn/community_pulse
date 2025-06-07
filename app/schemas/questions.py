from pydantic import BaseModel, Field
from typing import Optional


class QuestionCreate(BaseModel):
    text: str = Field(..., description="Text of the question", max_length=200, min_length=10)
    category_id: int = Field(..., description="Category id of the question")


class MessageResponse(BaseModel):
    message: str

    class Config:
        from_attributes = True


class CategoryBase(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    name: str = Field(..., description="Name of the category")


class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class QuestionResponse(BaseModel):
    id: int
    text: str
    category: Optional[CategoryResponse]


class QuestionDelete(BaseModel):
    question_id: int = Field(...)


class QuestionUpdate(QuestionCreate):
    question_id: int = Field(...)
    text: str = Field(..., description="Type new text")


class QuestionSchema(BaseModel):
    id: int
    text: str
    category_id: Optional[CategoryBase]


