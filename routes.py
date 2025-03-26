from flask import render_template, request, jsonify, make_response

from models import Merchandise
from utils import serialize_merch

def register_routes(app, db):


    # Home route to test server
    @app.route('/')
    def index():
        all_merchandise = Merchandise.query.all()
        merch_list = [serialize_merch(merch) for merch in all_merchandise]
        return jsonify(merch_list)

    # ---------------- CREATE Merchandise ----------------
    @app.route('/api/merchandise', methods=['POST'])
    def create_merchandise():
        try:
            data = request.get_json()
            new_item = Merchandise(
                name=data['name'],
                category=data['category'],
                price=data['price'],
                description=data['description']
            )
            db.session.add(new_item)
            db.session.commit()
            return jsonify({'message': 'Merchandise created successfully', 'id': new_item.id}), 201
        except Exception as e:
            return make_response(jsonify({'message': 'Error creating merchandise', 'error': str(e)}), 500)

    # ---------------- READ All Merchandise ----------------
    @app.route('/api/merchandise', methods=['GET'])
    def get_all_merchandise():
        try:
            all_merchandise = Merchandise.query.all()
            merch_list = [serialize_merch(merch) for merch in all_merchandise]
            return jsonify(merch_list), 200
        except Exception as e:
            return make_response(jsonify({'message': 'Error fetching merchandise', 'error': str(e)}), 500)

    # ---------------- READ Single Merchandise ----------------
    @app.route('/api/merchandise/<id>', methods=['GET'])
    def get_merchandise(id):
        try:
            item = Merchandise.query.filter_by(id=id).first()
            if item:
                return jsonify(serialize_merch(item)), 200
            else:
                return make_response(jsonify({'message': 'Merchandise not found'}), 404)
        except Exception as e:
            return make_response(jsonify({'message': 'Error fetching merchandise', 'error': str(e)}), 500)

    # ---------------- UPDATE Merchandise ----------------
    @app.route('/api/merchandise/<id>', methods=['PUT'])
    def update_merchandise(id):
        try:
            item = Merchandise.query.filter_by(id=id).first()
            if item:
                data = request.get_json()
                item.name = data['name']
                item.category = data['category']
                item.price = data['price']
                item.description = data['description']
                db.session.commit()
                return jsonify({'message': 'Merchandise updated successfully'}), 200
            else:
                return make_response(jsonify({'message': 'Merchandise not found'}), 404)
        except Exception as e:
            return make_response(jsonify({'message': 'Error updating merchandise', 'error': str(e)}), 500)

    # ---------------- DELETE Merchandise ----------------
    @app.route('/api/merchandise/<id>', methods=['DELETE'])
    def delete_merchandise(id):
        try:
            item = Merchandise.query.filter_by(id=id).first()
            if item:
                db.session.delete(item)
                db.session.commit()
                return jsonify({'message': 'Merchandise deleted successfully'}), 200
            else:
                return make_response(jsonify({'message': 'Merchandise not found'}), 404)
        except Exception as e:
            return make_response(jsonify({'message': 'Error deleting merchandise', 'error': str(e)}), 500)