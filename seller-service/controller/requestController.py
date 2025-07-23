from service.requestService import RequestService
from flask import jsonify

class RequestController:

    def handle_seller_blanket_request(data):
        try:
            response = RequestService.process_seller_request(data)
            return jsonify({"message": "Request processed successfully", "saved_requests": response}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
     


    @staticmethod
    def approveRequest(request_id):
        return RequestService.approveRequest(request_id)

    @staticmethod
    def getAllRequestHistory():
        return RequestService.getAllRequestHistory()