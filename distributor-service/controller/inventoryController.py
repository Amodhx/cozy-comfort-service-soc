from service.inventoryService import InventoryService


class InventoryController:

    def update_distributor_stock(data):
        blanket_name = data.get('blanket_name')
        blanket_size = data.get('blanket_size')
        add_count = data.get('add_count')

        return InventoryService.update_distributor_inventory(blanket_name, blanket_size, add_count)
    
    def getAllInventoryData():
        return InventoryService.getAllDistributorInventories()