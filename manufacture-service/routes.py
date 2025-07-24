from flask import Blueprint, request, jsonify

api_routes = Blueprint('api_routes', __name__)

@api_routes.route('/getAllInventories', methods=['GET'])
def getAllInventoryList():
    return "Hello Hello"