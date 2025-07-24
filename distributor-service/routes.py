from flask import Blueprint, request, jsonify
from controller.blanketController import BlanketController
from controller.inventoryController import InventoryController
from controller.requestController import RequestController
api_routes = Blueprint('api_routes', __name__)


@api_routes.route('/getAllRequestHistoryCompleted',methods=['GET'])
def get_all_completed_request_history():
    try:
        data = RequestController.getAllCompltedRequests()
        return jsonify({
            "message": "Filtered Requsts fetched successfully",
            "status": "success",
            "data": data
        })
    except Exception as e:
        return jsonify({"message": str(e), "status": "error"}), 500


@api_routes.route('/getAllRequestHistoryNotCompleted',methods=['GET'])
def get_all_request_history():
    try:
        data = RequestController.getAllInCompltedRequests()
        return jsonify({
            "message": "Filtered Requsts fetched successfully",
            "status": "success",
            "data": data
        })
    except Exception as e:
        return jsonify({"message": str(e), "status": "error"}), 500

@api_routes.route('/approveRequest', methods=['POST'])
def approve_request():
    try:
        data = request.get_json()
        response = RequestController.approveRequest(data)
        return jsonify({
            "message": "Requsts Approved successfully",
            "status": "success",
            "data": response
        })
    except Exception as e:
        return jsonify({"message": str(e), "status": "error"}), 500
    
@api_routes.route('/sendReqtoManufactor', methods=['POST'])
def send_manufactor_requests():
    try:
        data = request.get_json()

        result = RequestController.sendRequestToManufactor(data)
        return jsonify({"message": "Request Sent", "status": "success"}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e), "status": "error"}), 500
    

@api_routes.route('/updateDistributorStockCount', methods=['POST'])
def update_distributor_stock_count():
    try:
        data = request.get_json()
        result = InventoryController.update_distributor_stock(data)

        return jsonify(result), 200 if result["status"] == "success" else 400

    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 400



@api_routes.route('/getAllInventories', methods=['GET'])
def getAllInventoryList():
    try:
        data = InventoryController.getAllInventoryData()
        return jsonify({
            "message": "Filtered Inventory fetched successfully",
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