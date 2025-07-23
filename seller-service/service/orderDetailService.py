from config.dbConfig import get_connection

class OrderDetailsService:

    @staticmethod
    def saveOrderDetail(orderDetail):
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO OrderDetails (order_id, seller_stock_id, qty, price)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (
            orderDetail.order_id,
            orderDetail.seller_stock_id,
            orderDetail.qty,
            orderDetail.price
        ))

        conn.commit()
        cursor.close()
        conn.close()
