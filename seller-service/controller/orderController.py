from model.orderModel import OrderModel
from service.orderService import OrderService
from service.customerService import CustomerService
from model.orderDetailsModel import OrderDetailsModel
from service.orderDetailService import OrderDetailsService
from model.customerModel import CustomerModel
from service.inventoryService import InventoryService
from service.blanketService import BlanketService

class OrderController:
   
   def getAllOrders():
       orders = OrderService.getAllOrderHistory()
       return orders

   def saveOrder(customerData, orderData):
        customerToSave = CustomerModel(
            0,
            customerData.get("name"),
            customerData.get("email"),
            customerData.get("contact_number"))
        customer = CustomerService.saveCustomer(customerToSave)

        order = OrderModel(
            customer_id=customer.customer_id,
            total_price=orderData.get("total_price"),
            total_item_count=orderData.get("total_item_count")
        )
        saved_order_id = OrderService.saveOrder(order)
        items = orderData.get("items", [])
        for item in items:
            blanket_model = item.get("Blanket_Model")
            size = item.get("Size")
            qty = item.get("qty")


            blanket = BlanketService.get_blanket_by_model_and_size(blanket_model,size)
            blanket_id = blanket['blanket_id']
            stock_id = InventoryService.get_seller_stock_id_by_blanket_id(blanket_id)
            price = qty * blanket['price']

            detail = OrderDetailsModel(
                order_id=saved_order_id,
                seller_stock_id=stock_id,
                qty=qty,
                price=price
            )
            OrderDetailsService.saveOrderDetail(detail)

            current_stock = InventoryService.get_seller_stock_count(stock_id)
            if current_stock >= qty:
                new_qty = current_stock - qty
                InventoryService.reduceInventory(stock_id, new_qty)
            else:
                print(f"Insufficient stock for seller_stock_id: {stock_id}")

        return saved_order_id
