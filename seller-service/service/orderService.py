from model.orderModel import OrderModel
from config.dbConfig import get_connection
from datetime import datetime
class OrderService:

    def getAllOrderHistory():
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = """
                SELECT 
                    o.order_id, o.customer_id, o.date, o.total_price, o.total_item_count,
                    c.name AS customer_name, c.contact_number, c.email
                FROM `Order` o
                JOIN Customer c ON o.customer_id = c.customer_id
                ORDER BY o.date DESC
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            orders = []
            columns = [col[0] for col in cursor.description]
            for row in rows:
                orders.append(dict(zip(columns, row)))

            return orders
        except Exception as e:
            print("Error fetching orders with customer info:", e)
            return []
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def saveOrder(order: OrderModel):
        connection = get_connection()
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO `Order` (customer_id, date, total_price, total_item_count)
        VALUES (%s, %s, %s, %s)
        """

        current_date = datetime.today().strftime('%Y-%m-%d')
        cursor.execute(insert_query, (order.customer_id, current_date, order.total_price, order.total_item_count))
        connection.commit()

        order_id = cursor.lastrowid
        cursor.close()
        connection.close()

        return order_id
