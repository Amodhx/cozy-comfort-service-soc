from config.dbConfig import get_connection

class InventoryService:

    from config.dbConfig import get_connection

class InventoryService:

    @staticmethod
    def get_seller_stock_id_by_blanket_id(blanket_id):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = """
                SELECT stock_id FROM Inventory
                WHERE blanket_id = %s AND stock_type = 'SELLER'
                LIMIT 1
            """
            cursor.execute(query, (blanket_id,))
            result = cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print("Error fetching seller stock id:", e)
            return None
        finally:
            cursor.close()
            conn.close()


    def get_seller_stock_count(inventory_id):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = """
                SELECT qty FROM Inventory
                WHERE stock_id = %s AND stock_type = 'SELLER'
            """
            cursor.execute(query, (inventory_id,))
            result = cursor.fetchone()
            return result[0] if result else 0
        except Exception as e:
            print("Error fetching seller stock count:", e)
            return 0
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def saveInventory(inventory):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            insert_query = """
                INSERT INTO Inventory (blanket_id, qty, stock_type)
                VALUES (%s, %s, %s)
            """
            cursor.execute(insert_query, (
                inventory.blanket_id,
                inventory.qty,
                inventory.stock_type
            ))
            conn.commit()
            return "Inventory entry saved successfully!"
        except Exception as e:
            print("Error while saving inventory:", e)
            return "Error occurred while saving inventory"
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def reduceInventory(seller_stock_id, reduce_qty):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            # Get current quantity
            select_query = "SELECT qty FROM Inventory WHERE stock_id = %s"
            cursor.execute(select_query, (seller_stock_id,))
            result = cursor.fetchone()
            if not result:
                return "Inventory not found"
            
            current_qty = result[0]
            if current_qty < reduce_qty:
                return "Not enough inventory"
            
            # Update quantity
            update_query = "UPDATE Inventory SET qty = qty - %s WHERE stock_id = %s"
            cursor.execute(update_query, (current_qty-reduce_qty, seller_stock_id))
            conn.commit()
            return "Inventory updated successfully"
        except Exception as e:
            print("Error while reducing inventory:", e)
            return "Error occurred while reducing inventory"
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def getInventoryByBlanket(blanket_id):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = """
                SELECT * FROM Inventory
                WHERE blanket_id = %s
            """
            cursor.execute(query, (blanket_id,))
            results = cursor.fetchall()
            return [dict(zip([col[0] for col in cursor.description], row)) for row in results]
        except Exception as e:
            print("Error while fetching inventory:", e)
            return []
        finally:
            cursor.close()
            conn.close()
