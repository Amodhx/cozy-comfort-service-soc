from flask import Blueprint, request, jsonify
from datetime import date
import os
from werkzeug.utils import secure_filename
from controller.blanketController import BlanketController
from controller.orderController import OrderController
from controller.requestController import RequestController

UPLOAD_FOLDER = 'uploads'  # create this folder if not exists
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
BASE_URL = 'http://localhost:3000/uploads/'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

api_routes = Blueprint('api_routes', __name__)

@api_routes.route('/blanket/saveBlanket', methods=['POST'])
def saveBlanket():
    try:
        model = request.form.get('model')
        material = request.form.get('material')
        price = request.form.get('price')
        description = request.form.get('description')
        size = request.form.get('size')

        image_file = request.files.get('image')
        image_url = None

        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            image_file.save(image_path)

            image_url = BASE_URL + filename
        else:
            return jsonify({"error": "Valid image file is required"}), 400
        responseData = BlanketController.saveBlanket({
            "model": model,
            "material": material,
            "price": price,
            "description": description,
            "size": size,
            "image": image_url
        })
        return jsonify(responseData), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

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


@api_routes.route('/request/sellerDistributorRequest', methods=['POST'])
def saveRequest():
    data = request.get_json()
    result = RequestController.handle_seller_blanket_request(data)
    return result


@api_routes.route('/placeOrder', methods=['POST'])
def placeOrder():
    data = request.get_json()

    customerData = {
        "name": data.get("customer_name"),
        "email": data.get("email"),
        "contact_number": data.get("contact_number")
    }

    orderData = {
        "total_price": data.get("total_price"),
        "total_item_count": data.get("total_item_count"),
        "items": data.get("Items", [])
    }

    saved_order = OrderController.saveOrder(customerData, orderData)

    return jsonify({
        "message": "Order placed successfully",
        "order": saved_order
    })

@api_routes.route('/getAllOrders', methods=['GET'])
def getAllOrders():
    orders = OrderController.getAllOrders()

    return jsonify({"orders": orders})


@api_routes.route('/request/approveStock', methods=["POST"])
def setCompleteDestributorOrder():
    data = request.get_json()
    request_id = data.get("request_id")

    result = RequestController.approveRequest(request_id)
    return jsonify(result)


@api_routes.route('/request/getAllRequestHistory', methods=['GET'])
def getAllRequestHistory():
    result = RequestController.getAllRequestHistory()
    return jsonify(result)


    
