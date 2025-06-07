from flask import Blueprint, request, jsonify
from app.models import db, Category
from pydantic import ValidationError
from app.schemas.questions import CategoryBase, CategoryResponse, CategoryCreate


categories_bp = Blueprint('categories', __name__, url_prefix='/categories')

# getting all categories
@categories_bp.route('/', methods=['GET'])
def get_category():
    category = Category.query.all()
    # refactoring all objects into a list with dictionary
    categories_data = [CategoryResponse.model_validate(obj).model_dump() for obj in category]
    return jsonify(categories_data)

# creating a new category
@categories_bp.route('/', methods=['POST'])
def create_category():
    data = request.get_json()
    try:
        category_data = CategoryCreate(**data)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    # checking if category with this name already exists
    exists = Category.query.filter_by(name=category_data.name).first()
    if exists:
        return jsonify({'message': '| Category already exists |'}), 400

    # trying to create a new category
    try:
        category = Category(name=category_data.name)
        db.session.add(category)
        db.session.commit()
        return jsonify({'message': '| Category created |'}, {'id': category.id, 'name': category.name}), 201

    except ValidationError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '| Something gone wrong. Try again later |'}), 400

# getting a certain category
@categories_bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = Category.query.get(category_id)
    # checking if such category exists
    if not category or category is None:
        return jsonify({'message': '| Category not found |'}), 404
    return jsonify({CategoryResponse.model_validate(category).model_dump()}), 200

# updating a category by category ID
@categories_bp.route('/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    category = Category.query.get(category_id)
    # checking if such category exists
    if not category or category is None:
        return jsonify({'message': '| Category not found |'}), 404
    data = request.get_json()
    if 'name' in data:
        category.name = data['name']
        db.session.commit()
        return jsonify({'message': '| Category updated |'}), 200
    else:
        return jsonify(CategoryResponse.model_validate(category).model_dump()), 400

# deleting a category by category ID
@categories_bp.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = Category.query.get(category_id)
    # checking if such category exists
    if not category or category is None:
        return jsonify({'message': '| Category not found |'}), 404

    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': '| Category was deleted |'}), 200