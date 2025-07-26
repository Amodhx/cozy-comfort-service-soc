from service.requestService import RequestService
class RequestController:

    def acceptDistributorRequest(request_id):
        return RequestService.acceptDistributorRequest(request_id)


    def getAllCompletedDistributorRequests():
        return RequestService.getAllCompletedDistributorRequests()
    @staticmethod
    def getAllNotCompletedRequests():
        return RequestService.getAllNotCompletedRequests()