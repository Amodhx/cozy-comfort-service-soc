from flask import Blueprint, request, jsonify
from controller.blanketController import BlanketController
from controller.productionController import ProductionController
import os
from werkzeug.utils import secure_filename


api_routes = Blueprint('api_routes', __name__)

UPLOAD_FOLDER = 'uploads'  # create this folder if not exists
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
BASE_URL = 'http://localhost:3001/uploads/'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@api_routes.route('/blanket/saveBlanket', methods=['POST'])
def saveBlanket():
    try:
        model = request.form.get('model')
        material = request.form.get('material')
        price = request.form.get('price')
        description = request.form.get('description')
        size = request.form.get('size')
        capacity = request.form.get('stockCapacity')

        image_file = request.files.get('image')
        image_url = None

        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            image_file.save(image_path)

            image_url = BASE_URL + filename
        else:
            return jsonify({"error": "Valid image file is required"}), 400
        responseData = BlanketController.saveBlanketData({
            "model": model,
            "material": material,
            "price": price,
            "description": description,
            "size": size,
            "image": image_url,
            "stockCapacity" : capacity
        })
        return jsonify(responseData), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_routes.route('/updateProductionCount', methods=['POST'])
def update_production_count():
    data = request.get_json()
    try:
        data = ProductionController.updateProductionCount(data)
        return jsonify({
            "message": "Production count updated successfully",
            "status": "success",
            "data": data
        })
    except Exception as e:
        return jsonify({"message": str(e), "status": "error"}), 500

@api_routes.route('/getAllProductionValues', methods=['GET'])
def get_all_production_values():
    try:
        data = ProductionController.getAllProductionValues()
        return jsonify({
            "message": "Production values fetched successfully",
            "status": "success",
            "data": data
        })
    except Exception as e:
        return jsonify({"message": str(e), "status": "error"}), 500

@api_routes.route('/blanket/getAllBlanket', methods=['GET'])
def getAllBlankets():
    try:
        data = BlanketController.getAllBlanketData()
        return jsonify({
            "message": "Filtered blankets fetched successfully",
            "status": "success",
            "data": data
        })
    except Exception as e:
        return jsonify({"message": str(e), "status": "error"}), 500

@api_routes.route('/blanket/filter', methods=['GET'])
def filter_blankets():
    size = request.args.get('size')
    material = request.args.get('material')

    try:
        if size and not material:
            data = BlanketController.getAllBlanketBySize(size)
        elif size and material:
            data = BlanketController.getAllBlanketWithSizeAndMaterial(size, material)
        else:
            return jsonify({"message": "Size is required", "status": "error"}), 400

        return jsonify({
            "message": "Filtered blankets fetched successfully",
            "status": "success",
            "data": data
        })
    except Exception as e:
        return jsonify({"message": str(e), "status": "error"}), 500