from config.dbConfig import get_connection

class BlanketService:

    def saveBlanket(blanket):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            insert_blanket_query = """
                INSERT INTO BlanketModel (model, material, price, description, size, image)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_blanket_query, (
                blanket.model,
                blanket.material,
                blanket.price,
                blanket.description,
                blanket.size,
                blanket.image
            ))

            blanket_id = cursor.lastrowid

            insert_stock_query = """
                INSERT INTO ProductionStock (total, blanket_id)
                VALUES (%s, %s)
            """
            cursor.execute(insert_stock_query, (blanket.productionCapacity, blanket_id))

            conn.commit()
            return {"message": "Blanket and stock saved successfully", "status": "success"}
        
        except Exception as e:
            print("Error while saving blanket and stock:", e)
            return {"message": "Error saving blanket and stock", "status": "fail", "error": str(e)}
        
        finally:
            cursor.close()
            conn.close()


    def get_all_blanket_data():
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = "SELECT * FROM BlanketModel"
            cursor.execute(query)
            results = cursor.fetchall()
            return [dict(zip([col[0] for col in cursor.description], row)) for row in results]
        except Exception as e:
            print("Error:", e)
            return []
        finally:
            cursor.close()
            conn.close()

    def get_manufactrer_stock_count(blanket_id):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = """
                SELECT SUM(qty) FROM Inventory 
                WHERE blanket_id = %s AND stock_type = 'MANUFACTURER'
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