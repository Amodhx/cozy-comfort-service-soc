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

    @staticmethod
    def approveRequest(request_id):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Update status to APPROVED
            query = """
                UPDATE Seller_Distributor_Request
                SET seller_distributor_status = 'APPROVED'
                WHERE seller_distributor_request_id = %s
            """
            cursor.execute(query, (request_id,))
            conn.commit()

            return {"status": "success", "message": "Request approved successfully"}
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
