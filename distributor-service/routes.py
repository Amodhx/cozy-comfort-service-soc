from flask import Blueprint, request, jsonify


api_routes = Blueprint('api_routes', __name__)

@api_routes.route('/hello', methods=['GET'])
def hello():
    return jsonify(message="Hello from /cozy_comfort/hello!")

@api_routes.route('/helloSave', methods=['POST'])
def saveValues():
    data = request.get_json()
    return jsonify(data)
    
