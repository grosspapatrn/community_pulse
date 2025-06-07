from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from app.models.question import Question
from app.schemas.questions import (
    CategoryBase, QuestionCreate, QuestionResponse, QuestionDelete,
    QuestionUpdate, QuestionSchema, MessageResponse)
from app.schemas.common import MessageResponse
from app.models import db

questions_bp = Blueprint('questions', __name__, url_prefix='/questions')
@questions_bp.route('/', methods=['GET'])
def get_questions():
    questions = Question.query.all()
    serialized = [QuestionSchema(id=question.id, text=question.text, category_id=question.category_id).model_dump() for question in questions]

    if questions:
        return jsonify(MessageResponse(message=serialized).model_dump()), 200
    else:
        return jsonify(MessageResponse(message="No questions found").model_dump()), 404


@questions_bp.route('/', methods=['POST'])
def create_question():
    input_data = request.get_json()
    try:
        question_data = QuestionCreate(**input_data)
        question = Question(text=question_data.text, category_id=question_data.category_id)
        db.session.add(question)
        db.session.commit()

        return jsonify(MessageResponse(message="Your question was created!").model_dump()), 200

    except ValidationError as e:
        return jsonify({'error': e.errors}), 400

@questions_bp.route('/<int:id>', methods=['GET'])
def get_question(id):
    question = Question.query.get(id)

    if question:
        return jsonify(MessageResponse(message=QuestionSchema(id=question.id, text=question.text, category_id=question.category_id).model_dump()).model_dump())
    else:
        return jsonify(MessageResponse(message=f"No question with id {id} was found.").model_dump())

@questions_bp.route('/<int:id>', methods=['PUT'])
def update_question(id):
    question = Question.query.get(id)
    input_data = request.get_json()

    if question:
        try:
            updated_data = QuestionUpdate(**input_data)
            question.text = updated_data.text
            db.session.commit()
            return jsonify(MessageResponse(message=f"The question with id {id} was updated.").model_dump()), 200
        except ValidationError as e:
            return jsonify({'error': e.errors}), 400
    else:
        return jsonify(MessageResponse(message=f"No question with id {id} was found.").model_dump()), 404

@questions_bp.route('/<int:id>', methods=['DELETE'])
def delete_question(id):
    question = Question.query.get(id)

    if question:
        db.session.delete(question)
        db.session.commit()
        return jsonify(MessageResponse(message=f"The question with id {id} was deleted.").model_dump()), 200
    else:
        return jsonify(MessageResponse(message=f"No question with id {id} was found.").model_dump()), 404