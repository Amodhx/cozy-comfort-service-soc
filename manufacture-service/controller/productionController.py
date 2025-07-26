from service.productionService import ProductionService
class ProductionController:

    def getAllProductionValues():
        return ProductionService.getAllProductionValues()
    
    def updateProductionCount(data):
        # Logic to update production count would go here
        # This is a placeholder for the actual implementation
        production_stock_id = data.get("production_stock_id")
        total = data.get("total")
        result = ProductionService.update_production_total(production_stock_id, total)
        return result