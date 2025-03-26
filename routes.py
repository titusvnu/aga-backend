from flask import request, jsonify, make_response
from models import Merchandise, Image
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
                description=data['description'])

            images = data.get('images', [])
            for url in images:
                # Create an Image object for each URL, with purpose 'merchandise'
                img = Image(url=url, purpose='merchandise')
                new_item.images.append(img)  # Link it to the merchandise item


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
            return make_response(jsonify({'message': 'Error deleting merchandise', 'error': str(e)}), 500)\

    @app.route('/debug/images')
    def debug_images():
        images = Image.query.all()
        return jsonify([
            {'url': i.url, 'purpose': i.purpose, 'merchandise_id': i.merchandise_id}
            for i in images
        ])
    
    @app.route('/api/merchandise/<id>/images', methods=['POST'])
    def add_merch_images(id):
        try:
            item = Merchandise.query.filter_by(id=id).first()
            if not item:
                return jsonify({'message': 'Merchandise not found'}), 404

            data = request.get_json()
            image_urls = data.get('images', [])

            for url in image_urls:
                img = Image(url=url, purpose='merchandise', merchandise_id=item.id)
                db.session.add(img)

            db.session.commit()
            return jsonify({'message': 'Images added to merchandise successfully'}), 201
        except Exception as e:
            return make_response(jsonify({'message': 'Error adding images', 'error': str(e)}), 500)
    
    
    @app.route('/api/gallery-image', methods=['POST'])
    def upload_gallery_image():
        try:
            data = request.get_json()
            img = Image(url=data['url'], purpose='gallery')
            db.session.add(img)
            db.session.commit()
            return jsonify({'message': 'Gallery image saved successfully'}), 201
        except Exception as e:
            return jsonify({'message': 'Error', 'error': str(e)}), 500

    @app.route('/api/gallery', methods=['GET'])
    def get_gallery_images():
        gallery_images = Image.query.filter_by(purpose='gallery').all()
        return jsonify([img.url for img in gallery_images])
