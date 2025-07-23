import mysql.connector
from config.dbConfig import get_connection  # Your DB connection function
from model.customerModel import CustomerModel

class CustomerService:

    def saveCustomer(customerData : CustomerModel):
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO Customer (name, email, contact_number)
            VALUES (%s, %s, %s)
        """
        values = (customerData.name,customerData.email, customerData.contact_number)
        cursor.execute(query, values)
        connection.commit()

        customer_id = cursor.lastrowid  # Get auto-generated ID
        cursor.close()
        connection.close()

        return CustomerModel(customer_id, customerData.name,customerData.email, customerData.contact_number)
