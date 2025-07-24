from config.dbConfig import get_connection  

class InventoryService:

    def update_distributor_inventory(blanket_name, blanket_size, add_count):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Step 1: Get blanket_id using model and size
            get_blanket_query = """
                SELECT blanket_id FROM BlanketModel 
                WHERE model = %s AND size = %s
            """
            cursor.execute(get_blanket_query, (blanket_name, blanket_size))
            result = cursor.fetchone()

            if not result:
                return {"status": "error", "message": "Blanket not found."}

            blanket_id = result[0]

            # Step 2: Check if blanket already in distributor inventory
            check_inventory_query = """
                SELECT qty FROM Inventory 
                WHERE blanket_id = %s AND stock_type = 'DISTRIBUTOR'
            """
            cursor.execute(check_inventory_query, (blanket_id,))
            existing = cursor.fetchone()

            if existing:
                new_qty = existing[0] + int(add_count)
                update_query = """
                    UPDATE Inventory SET qty = %s 
                    WHERE blanket_id = %s AND stock_type = 'DISTRIBUTOR'
                """
                cursor.execute(update_query, (new_qty, blanket_id))
            else:
                insert_query = """
                    INSERT INTO Inventory (blanket_id, qty, stock_type) 
                    VALUES (%s, %s, 'DISTRIBUTOR')
                """
                cursor.execute(insert_query, (blanket_id, add_count))

            conn.commit()
            return {"status": "success", "message": "Inventory updated successfully."}

        except Exception as e:
            print("Error in update_distributor_inventory:", e)
            return {"status": "error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()

            
    @staticmethod
    def getAllDistributorInventories():
        try:
            conn = get_connection()
            cursor = conn.cursor()

            query = """
                SELECT 
                    i.stock_id,
                    i.blanket_id,
                    b.model,
                    b.material,
                    b.price,
                    b.description,
                    b.size,
                    b.image,
                    i.qty,
                    i.stock_type
                FROM Inventory i
                JOIN BlanketModel b ON i.blanket_id = b.blanket_id
                WHERE i.stock_type = 'DISTRIBUTOR'
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            inventories = []
            for row in rows:
                inventories.append({
                    "stock_id": row[0],
                    "blanket_id": row[1],
                    "model": row[2],
                    "material": row[3],
                    "price": float(row[4]),
                    "description": row[5],
                    "size": row[6],
                    "image": row[7],
                    "qty": row[8],
                    "stock_type": row[9]
                })

            return {"status": "success", "data": inventories}

        except Exception as e:
            print("Error fetching distributor inventories:", e)
            return {"status": "error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()
