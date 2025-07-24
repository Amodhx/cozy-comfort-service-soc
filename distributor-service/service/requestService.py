from config.dbConfig import get_connection

class RequestService:
    
    def sendReqToManu(data):
        try:
            blanket_id = data.get("blanket_id")
            qty = data.get("qty")

            print("Sending request to manufacturer for blanket_id:", blanket_id, "qty:", qty)

            conn = get_connection()
            cursor = conn.cursor()

            insert_query = """
                INSERT INTO Distributor_Manufactor_Request (blanket_id, qty, distributor_manufactor_status)
                VALUES (%s, %s, 'PENDING')
            """
            cursor.execute(insert_query, (blanket_id, qty))
            conn.commit()

            return {"status": "success", "message": "Request sent to manufacturer successfully."}

        except Exception as e:
            print("Error sending request to manufacturer:", e)
            return {"status": "error", "message": str(e)}

        finally:
            cursor.close()
            conn.close()

    def approveRequest(data):
        try:
            request_id = data.get("request_id")

            conn = get_connection()
            cursor = conn.cursor()

            update_query = """
                UPDATE Seller_Distributor_Request
                SET seller_distributor_status = 'APPROVED'
                WHERE seller_distributor_request_id = %s
            """
            cursor.execute(update_query, (request_id))
            conn.commit()

            if cursor.rowcount == 0:
                return {"status": "error", "message": "No matching pending request found."}

            return {"status": "success", "message": "Request approved successfully."}

        except Exception as e:
            print("Error approving request:", e)
            return {"status": "error", "message": str(e)}

        finally:
            cursor.close()
            conn.close()


    def getAllIncompleteSellerRequests():
        try:
            conn = get_connection()
            cursor = conn.cursor()

            query = """
                SELECT 
                    r.seller_distributor_request_id,
                    r.blanket_id,
                    r.qty,
                    r.seller_distributor_status,
                    b.model,
                    b.material,
                    b.size,
                    b.price
                FROM Seller_Distributor_Request r
                JOIN BlanketModel b ON r.blanket_id = b.blanket_id
                WHERE r.seller_distributor_status IN ('PENDING')
            """

            cursor.execute(query)
            rows = cursor.fetchall()

            results = []

            for row in rows:
                request_id = row[0]
                blanket_id = row[1]
                request_qty = row[2]

                # Check inventory for that blanket under DISTRIBUTOR type
                stock_query = """
                    SELECT qty FROM Inventory
                    WHERE blanket_id = %s AND stock_type = 'DISTRIBUTOR'
                """
                cursor.execute(stock_query, (blanket_id,))
                stock_result = cursor.fetchone()

                stock_qty = stock_result[0] if stock_result else 0

                button_text = "I Accept" if stock_qty >= request_qty else "Request from Manufacturer"

                results.append({
                    "seller_distributor_request_id": request_id,
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
            print("Error fetching incomplete seller requests:", e)
            return {"status": "error", "message": str(e)}

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def getAllCompletedRequests():
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
            approved_requests = cursor.fetchall()

            return {"status": "success", "data": approved_requests}

        except Exception as e:
            print("Error getting completed requests:", e)
            return {"status": "error", "message": str(e)}

        finally:
            cursor.close()
            conn.close()
