from config.dbConfig import get_connection
from service.blanketService import BlanketService

class RequestService:

    def process_seller_request(data):
        model = data.get("Blanket_Model")
        sizes = data.get("Sizes")
        qtys = data.get("qty")

        if not model or not sizes or not qtys:
            raise ValueError("Missing data fields")

        saved = []
        db = get_connection()
        cursor = db.cursor()

        for size, qty in zip(sizes, qtys):
            if qty <= 0:
                continue

            blanket = BlanketService.get_blanket_by_model_and_size(model, size)
            if blanket is None:
                print(f"No blanket found for model: {model} and size: {size}")
                continue

            blanket_id = blanket['blanket_id']

            
            cursor.execute("""
                INSERT INTO seller_distributor_request (blanket_id, qty, seller_distributor_status)
                VALUES (%s, %s, %s)
            """, (blanket_id, qty, "PENDING"))

            saved.append({"blanket_id": blanket_id, "qty": qty})

        db.commit()
        cursor.close()
        db.close()

        return saved

    def approveRequest(request_id):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # 1. Update status to APPROVED
            update_query = """
                UPDATE Seller_Distributor_Request
                SET seller_distributor_status = 'APPROVED'
                WHERE seller_distributor_request_id = %s
            """
            cursor.execute(update_query, (request_id,))
            conn.commit()

            # 2. Fetch blanket_id and qty of this request
            select_query = """
                SELECT blanket_id, qty FROM Seller_Distributor_Request
                WHERE seller_distributor_request_id = %s
            """
            cursor.execute(select_query, (request_id,))
            result = cursor.fetchone()

            if not result:
                return {"status": "error", "message": "Request not found."}

            blanket_id, qty = result

            # 3. Check if entry exists in Inventory with stock_type='SELLER'
            check_query = """
                SELECT stock_id, qty FROM Inventory
                WHERE blanket_id = %s AND stock_type = 'SELLER'
            """
            cursor.execute(check_query, (blanket_id,))
            existing = cursor.fetchone()

            if existing:
                # Entry exists → Update the qty
                stock_id, current_qty = existing
                new_qty = current_qty + qty
                update_inventory_query = """
                    UPDATE Inventory SET qty = %s WHERE stock_id = %s
                """
                cursor.execute(update_inventory_query, (new_qty, stock_id))
            else:
                # Entry doesn't exist → Insert new row
                insert_inventory_query = """
                    INSERT INTO Inventory (blanket_id, qty, stock_type)
                    VALUES (%s, %s, 'SELLER')
                """
                cursor.execute(insert_inventory_query, (blanket_id, qty))

            conn.commit()

            return {"status": "success", "message": "Request approved and inventory updated."}

        except Exception as e:
            print("Error approving request:", e)
            return {"status": "error", "message": str(e)}

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def getAllRequestHistory():
        try:
            conn = get_connection()
            cursor = conn.cursor()

            query = """
                SELECT r.seller_distributor_request_id, r.blanket_id, r.qty, r.seller_distributor_status,
                b.model, b.size
                FROM Seller_Distributor_Request r
                JOIN BlanketModel b ON r.blanket_id = b.blanket_id
                ORDER BY r.seller_distributor_request_id DESC
                """

            cursor.execute(query)
            rows = cursor.fetchall()

            columns = [col[0] for col in cursor.description]
            result = [dict(zip(columns, row)) for row in rows]
            return result
        except Exception as e:
            print("Error fetching request history:", e)
            return []
        finally:
            cursor.close()
            conn.close()
