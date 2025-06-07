from app.models import db
from datetime import datetime
from sqlalchemy.orm import validates

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    responses = db.relationship('Response', back_populates='question', lazy=True, cascade='all, delete-orphan')
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False, default=1)
    category = db.relationship("Category", back_populates="questions", lazy=True)
    statistic = db.relationship("Statistic", back_populates="question", lazy=True, uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f'Question: {self.text}'


class Statistic(db.Model):
    __tablename__ = 'statistics'

    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), primary_key=True)
    agree_count = db.Column(db.Integer, nullable=False, default=0)
    disagree_count = db.Column(db.Integer, nullable=False, default=0)

    question = db.relationship('Question', back_populates='statistic', lazy=True)

    def __repr__(self):
        return f'Statistic for Question {self.question_id}: {self.agree_count} agree, {self.disagree_count} disagree'


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    questions = db.relationship('Question', back_populates='category', lazy=True, cascade="all, delete-orphan")

    @validates('name')
    def validate_name(self, key, value):
        try:
            cleaned = value.strip()
            if not cleaned:
                raise ValueError('Category is not created. Field "Name" cannot be empty.')
            return cleaned
        except AttributeError:
            raise ValueError('Category is not created. Field "Name" cannot be empty.')

