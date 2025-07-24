from config.dbConfig import get_connection

class BlanketService:
    def get_distributor_stock_count(blanket_id):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = """
                SELECT SUM(qty) FROM Inventory 
                WHERE blanket_id = %s AND stock_type = 'DISTRIBUTOR'
            """
            cursor.execute(query, (blanket_id,))
            result = cursor.fetchone()
            return result[0] if result[0] is not None else 0
        except Exception as e:
            print("Error fetching seller stock count:", e)
            return 0
        finally:
            cursor.close()
            conn.close()

    def getAllBlanketBySize(size):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = "SELECT * FROM BlanketModel WHERE size = %s"
            cursor.execute(query, (size,))
            results = cursor.fetchall()
            return [dict(zip([col[0] for col in cursor.description], row)) for row in results]
        except Exception as e:
            print("Error:", e)
            return []
        finally:
            cursor.close()
            conn.close()

    def getAllBlanketWithSizeAndMaterial(size, material):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = "SELECT * FROM BlanketModel WHERE size = %s AND material = %s"
            cursor.execute(query, (size, material))
            results = cursor.fetchall()
            return [dict(zip([col[0] for col in cursor.description], row)) for row in results]
        except Exception as e:
            print("Error:", e)
            return []
        finally:
            cursor.close()
            conn.close()