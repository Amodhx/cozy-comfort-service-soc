from service.requestService import RequestService

class RequestController:
    def sendRequestToManufactor(data):
        return RequestService.sendReqToManu(data)
    def getAllCompltedRequests():
        return RequestService.getAllCompletedRequests()
    
    def getAllInCompltedRequests():
        return RequestService.getAllIncompleteSellerRequests()
    
    def approveRequest(data):
        return RequestService.approveRequest(data)