from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from app.models.response import Response
from app.schemas.common import MessageResponse
from app.schemas.responses import ResponseCreate, ResponseSchema, ResponseUpdate
from app.models import db

responses_bp = Blueprint('responses', __name__, url_prefix='/responses')

@responses_bp.route('/', methods=['GET'])
def get_responses():
    responses = Response.query.all()
    serialized = [ResponseSchema(question_text=r.question.text, is_agree=r.is_agree).model_dump() for r in responses]

    if responses:
        return jsonify(MessageResponse(message=serialized).model_dump()), 200
    else:
        return jsonify(MessageResponse(message="No responses found").model_dump()), 404
    

@responses_bp.route('/', methods=['POST'])
def create_response():
    input_data = request.get_json()
    try:
        response_data = ResponseCreate(**input_data)
        response = Response(question_id=response_data.question_id, is_agree=response_data.is_agree)
        db.session.add(response)
        db.session.commit()

        return jsonify(MessageResponse(message="Your response was created!").model_dump()), 200

    except ValidationError as e:
        return jsonify({'error': e.errors}), 400
    
@responses_bp.route('/<int:id>', methods=['GET'])
def get_response(id):
    response = Response.query.get(id)

    if response:
        return jsonify(MessageResponse(message=ResponseSchema(question_text=response.question.text, is_agree=response.is_agree).model_dump()).model_dump())
    else:
        return jsonify(MessageResponse(message=f"No response with id {id} was found.").model_dump())

@responses_bp.route('/<int:id>', methods=['PUT'])
def update_response(id):
    response = Response.query.get(id)
    input_data = request.get_json()

    if response:
        try:
            updated_data = ResponseUpdate(**input_data)
            response.is_agree = updated_data.is_agree
            response.question_id = updated_data.question_id

            db.session.commit()

            return jsonify(MessageResponse(message=f"The response with id {id} was updated.").model_dump()), 200
        except ValidationError as e:
            return jsonify({'error': e.errors}), 400
    else:
        return jsonify(MessageResponse(message=f"No response with id {id} was found.").model_dump()), 404

@responses_bp.route('/<int:id>', methods=['DELETE'])
def delete_response(id):
    response = Response.query.get(id)

    if response:
        db.session.delete(response)
        db.session.commit()

        return jsonify(MessageResponse(message=f"The response with id {id} was deleted.").model_dump()), 200
    else:
        return jsonify(MessageResponse(message=f"No response with id {id} was found.").model_dump()), 404
