class OrderDetailsModel:
    def __init__(self, order_id, seller_stock_id, qty, price):
        self.order_id = order_id
        self.seller_stock_id = seller_stock_id
        self.qty = qty
        self.price = price
