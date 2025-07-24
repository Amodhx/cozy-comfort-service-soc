from service.blanketService import  BlanketService
from model.blanketModel import BlanketModel

class BlanketController:
    def saveBlanket(data):
        dataToSave = BlanketModel(
            data.get('model'),
            data.get('material'),
            data.get('price'),
            data.get('description'),
            data.get('size'),
            data.get('image'))

        result = BlanketService.saveBlanket(dataToSave)

        return result
    
    def getAllBlanketBySize(size):
        blankets = BlanketService.getAllBlanketBySize(size)
        # Add seller stock count for each blanket
        for blanket in blankets:
            stock_count = BlanketService.get_seller_stock_count(blanket['blanket_id'])
            blanket['seller_stock_available_count'] = stock_count
        return blankets

    def getAllBlanketWithSizeAndMaterial(size, material):
        blankets = BlanketService.getAllBlanketWithSizeAndMaterial(size, material)
        # Add seller stock count for each blanket
        for blanket in blankets:
            stock_count = BlanketService.get_seller_stock_count(blanket['blanket_id'])
            blanket['seller_stock_available_count'] = stock_count
        return blankets
    
    def getAllBlanketdata():
        blankets = BlanketService.getAllBlanketData()
        for blanket in blankets:
            stock_count = BlanketService.get_seller_stock_count(blanket['blanket_id'])
            blanket['seller_stock_available_count'] = stock_count
        return blankets