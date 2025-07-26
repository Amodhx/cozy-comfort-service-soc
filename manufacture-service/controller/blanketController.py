from service.blanketService import BlanketService
from model.blanketModel import BlanketModel
class BlanketController:

    def saveBlanketData(data):
        dataToSave = BlanketModel(
            data.get('model'),
            data.get('material'),
            data.get('price'),
            data.get('description'),
            data.get('size'),
            data.get('image'),
            data.get('stockCapacity'))

        result = BlanketService.saveBlanket(dataToSave)

        return result

    def getAllBlanketData():
        blankets = BlanketService.get_all_blanket_data()
        for blanket in blankets:
            stock_count = BlanketService.get_manufactrer_stock_count(blanket['blanket_id'])
            blanket['manufactrer_stock_available_count'] = stock_count
        return blankets
    
    def getAllBlanketBySize(size):
        blankets = BlanketService.getAllBlanketBySize(size)
        # Add seller stock count for each blanket
        for blanket in blankets:
            stock_count = BlanketService.get_manufactrer_stock_count(blanket['blanket_id'])
            blanket['manufactrer_stock_available_count'] = stock_count
        return blankets

    def getAllBlanketWithSizeAndMaterial(size, material):
        blankets = BlanketService.getAllBlanketWithSizeAndMaterial(size, material)
        # Add seller stock count for each blanket
        for blanket in blankets:
            stock_count = BlanketService.get_manufactrer_stock_count(blanket['blanket_id'])
            blanket['manufactrer_stock_available_count'] = stock_count
        return blankets