from datetime import date

class OrderModel:
    def __init__(self,customer_id,total_price,total_item_count):
        self.customer_id = customer_id
        self.date = date.today().strftime('%Y-%m-%d')
        self.total_price = total_price
        self.total_item_count = total_item_count
