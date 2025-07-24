from flask import Blueprint, request, jsonify
from controller.blanketController import BlanketController

api_routes = Blueprint('api_routes', __name__)


@api_routes.route('/getAllRequestHistoryCompleted',methods=['GET'])
def get_all_completed_request_history():
    return "HELLO MAN"


@api_routes.route('/getAllRequestHistoryNotCompleted',methods=['GET'])
def get_all_request_history():
    return "Hello history"

@api_routes.route('/approveRequest', methods=['POST'])
def approve_request():
    try:
        data = request.get_json()
        request_id = data.get('request_id')

        print(f"Request ID received: {request_id}")

        return jsonify({"message": "Request ID received", "status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 400
    
@api_routes.route('/sendReqtoManufactor', methods=['POST'])
def send_manufactor_requests():
    try:
        data = request.get_json()

        blanket_id = data.get("blanket_id")
        qty = data.get("qty")

        print("Blanket ID:", blanket_id)
        print("Quantity:", qty)

        return jsonify({"message": "Request received", "status": "success"}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e), "status": "error"}), 500

@api_routes.route('/updateDistributorStockCount', methods=['POST'])
def update_distributor_stock_count():
    try:
        data = request.get_json()

        blanket_name = data.get('blanket_name')
        blanket_size = data.get('blanket_size')
        add_count = data.get('add_count')

        print(f"Blanket Name: {blanket_name}")
        print(f"Blanket Size: {blanket_size}")
        print(f"Add Count: {add_count}")

        return jsonify({"message": "Stock update received", "status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 400


@api_routes.route('/getAllInventories', methods=['GET'])
def getAllInventoryList():
    return "Hello Hello"

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