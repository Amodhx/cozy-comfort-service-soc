from config.dbConfig import get_connection

class RequestService:

    def acceptDistributorRequest(request_id):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            update_query = """
                UPDATE Distributor_Manufactor_Request
                SET distributor_manufactor_status = 'APPROVED'
                WHERE distributor_manufactor_request_id = %s
            """
            cursor.execute(update_query, (request_id,))
            conn.commit()

            if cursor.rowcount == 0:
                return {"status": "fail", "message": "Request not found or already approved."}

            return {"status": "success", "message": "Request accepted successfully"}

        except Exception as e:
            print("Error accepting distributor request:", e)
            return {"status": "error", "message": str(e)}

        finally:
            cursor.close()
            conn.close()

    def getAllCompletedDistributorRequests():
        try:
            conn = get_connection()
            cursor = conn.cursor()

            query = """
                SELECT 
                    r.distributor_manufactor_request_id,
                    r.qty,
                    r.distributor_manufactor_status,
                    b.blanket_id,
                    b.model,
                    b.material,
                    b.size,
                    b.price
                FROM Distributor_Manufactor_Request r
                JOIN BlanketModel b ON r.blanket_id = b.blanket_id
                WHERE r.distributor_manufactor_status = 'APPROVED'
            """

            cursor.execute(query)
            completed_requests = cursor.fetchall()

            results = []

            for row in completed_requests:
                results.append({
                    "distributor_manufactor_request_id": row[0],
                    "qty": row[1],
                    "status": row[2],
                    "blanket_id": row[3],
                    "model": row[4],
                    "material": row[5],
                    "size": row[6],
                    "price": row[7]
                })

            return {"status": "success", "data": results}

        except Exception as e:
            print("Error getting completed distributor requests:", e)
            return {"status": "error", "message": str(e)}

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def getAllNotCompletedRequests():
        try:
            conn = get_connection()
            cursor = conn.cursor()

            query = """
                SELECT 
                    r.distributor_manufactor_request_id,
                    r.blanket_id,
                    r.qty,
                    r.distributor_manufactor_status,
                    b.model,
                    b.material,
                    b.size,
                    b.price
                FROM Distributor_Manufactor_Request r
                JOIN BlanketModel b ON r.blanket_id = b.blanket_id
                WHERE r.distributor_manufactor_status = 'PENDING'
            """

            cursor.execute(query)
            rows = cursor.fetchall()

            results = []

            for row in rows:
                request_id = row[0]
                blanket_id = row[1]
                request_qty = row[2]

                # Check inventory under MANUFACTURER
                stock_query = """
                    SELECT qty FROM Inventory
                    WHERE blanket_id = %s AND stock_type = 'MANUFACTURER'
                """
                cursor.execute(stock_query, (blanket_id,))
                stock_result = cursor.fetchone()

                stock_qty = stock_result[0] if stock_result else 0

                # Update button text based on stock availability
                if stock_qty >= request_qty:
                    button_text = "I Accept"
                else:
                    button_text = "Can't give now"

                results.append({
                    "distributor_manufactor_request_id": request_id,
                    "blanket_id": blanket_id,
                    "qty": request_qty,
                    "status": row[3],
                    "model": row[4],
                    "material": row[5],
                    "size": row[6],
                    "price": row[7],
                    "button_text": button_text
                })

            return {"status": "success", "data": results}

        except Exception as e:
            print("Error fetching incomplete distributor requests:", e)
            return {"status": "error", "message": str(e)}

        finally:
            cursor.close()
            conn.close()
