from service.blanketService import BlanketService
class BlanketController:

    def getAllBlanketData():
        blankets = BlanketService.get_all_blanket_data()
        for blanket in blankets:
            stock_count = BlanketService.get_distributor_stock_count(blanket['blanket_id'])
            blanket['distributor_stock_available_count'] = stock_count
        return blankets
    
    def getAllBlanketBySize(size):
        blankets = BlanketService.getAllBlanketBySize(size)
        # Add seller stock count for each blanket
        for blanket in blankets:
            stock_count = BlanketService.get_distributor_stock_count(blanket['blanket_id'])
            blanket['distributor_stock_available_count'] = stock_count
        return blankets

    def getAllBlanketWithSizeAndMaterial(size, material):
        blankets = BlanketService.getAllBlanketWithSizeAndMaterial(size, material)
        # Add seller stock count for each blanket
        for blanket in blankets:
            stock_count = BlanketService.get_distributor_stock_count(blanket['blanket_id'])
            blanket['distributor_stock_available_count'] = stock_count
        return blankets