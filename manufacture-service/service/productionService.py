from config.dbConfig import get_connection

class ProductionService:

    def update_production_total(production_stock_id, total):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            query = "UPDATE ProductionStock SET total = %s WHERE production_stock_id = %s"
            cursor.execute(query, (total, production_stock_id))
            conn.commit()

            if cursor.rowcount == 0:
                return {"message": "No record found to update.", "status": "fail"}

            return {"message": "Production stock updated successfully", "status": "success"}

        except Exception as e:
            print("Error updating production stock:", e)
            return {"message": "Error updating production stock", "status": "error", "error": str(e)}
        finally:
            cursor.close()
            conn.close()


    @staticmethod
    def getAllProductionValues():
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = """
                SELECT 
                    b.blanket_id, b.model, b.material, b.price, b.description, b.size, b.image,
                    ps.production_stock_id, ps.total
                FROM BlanketModel b
                LEFT JOIN ProductionStock ps ON b.blanket_id = ps.blanket_id
            """

            cursor.execute(query)
            results = cursor.fetchall()

            data = []
            for row in results:
                record = dict(zip([col[0] for col in cursor.description], row))
                data.append(record)

            return data

        except Exception as e:
            print("Error fetching production values:", e)
            return []
        finally:
            cursor.close()
            conn.close()



