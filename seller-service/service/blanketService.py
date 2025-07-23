from config.dbConfig import get_connection

class BlanketService:
   
   def get_blanket_by_model_and_size(model, size):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            SELECT * FROM BlanketModel
            WHERE model = %s AND size = %s
            LIMIT 1
        """
        cursor.execute(query, (model, size))
        result = cursor.fetchone()
        if result:
            # Map result to dict with column names
            columns = [col[0] for col in cursor.description]
            return dict(zip(columns, result))
        else:
            return None
    except Exception as e:
        print("Error fetching blanket by model and size:", e)
        return None
    finally:
        cursor.close()
        conn.close()
   
   def get_seller_stock_count(blanket_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            SELECT SUM(qty) FROM Inventory 
            WHERE blanket_id = %s AND stock_type = 'SELLER'
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


   def saveBlanket(blanket):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            insert_query = """
                INSERT INTO BlanketModel (model, material, price, description, size, image)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            cursor.execute(insert_query, (
                blanket.model,
                blanket.material,
                blanket.price,
                blanket.description,
                blanket.size,
                blanket.image
            ))

            conn.commit()
            return "Blanket saved successfully!"
        except Exception as e:
            print("Error while saving blanket:", e)
            return "Error occurred while saving blanket"
        finally:
            cursor.close()
            conn.close()


    