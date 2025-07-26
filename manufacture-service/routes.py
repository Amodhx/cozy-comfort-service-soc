from flask import Blueprint, request, jsonify
from controller.blanketController import BlanketController

api_routes = Blueprint('api_routes', __name__)

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