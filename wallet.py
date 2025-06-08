from mysql.connector import Error
from connection import connection
from execute_query import execute_multiple_query

class Wallet:
    def __init__(self, user_id, address=None, balance=0):
        self.user_id = user_id
        self.address = address
        self.balance = balance
    
    def insert_wallet(self):
        """
        This function inserts user wallet data (user ID and address) into a MySQL database.
        
        :param user_id: The user ID is a unique identifier for a user in the system. It is used to associate
        wallet data with a specific user
        :param address: The address parameter is a string that represents the wallet address of a user. It
        is used as a value to be inserted into the "address" column of the "wallet" table in a MySQL
        database
        """
        
        try:
            conn = connection()
            
            insert_query = "INSERT INTO wallet (user_id, address, balance) VALUES (%s, %s, %s)"
            values = (self.user_id, self.address, self.balance)
            
            cursor = conn.cursor()
            cursor.execute(insert_query, values)
            conn.commit()
        except Error as e:
          print('An exception occurred', e)
          
    def select_wallet(self):
        """
        The function selects the user IDs from the "wallet" table in the "bot" database and returns
        them as a list.
        :return: a list of user IDs from the "wallet" table in the "bot" database.
        """
        try:
            conn = connection()
            
            select_query = "SELECT user_id FROM wallet LIMIT 1"
            cursor = conn.cursor()
            cursor.execute(select_query)
            users = cursor.fetchall()
            user_ids = [userid[0] for userid in users]    
            return user_ids
        
        except Error as e:
         print('An exception occurred', e)
         
    def select_wallet_by_user_id(self):
        """
        This function selects the wallet address associated with a given user ID from a MySQL database.
        
        :param user_id: The user ID is a unique identifier for a user in the database. This function selects
        the wallet address associated with the given user ID from the "wallet" table in the "bot"
        database
        :return: the wallet address of the user with the given user_id from the "wallet" table in the
        "bot" database.
        """
        try:
            select_query = "SELECT address, balance FROM wallet WHERE user_id = %s LIMIT 1"
            result = execute_multiple_query(select_query, (self.user_id,))
            
            if result:
                return result
            else:
                return(0,0)
        except Error as e:
            print('An exception occurred', e)
            return(None,None)
        
    def update_balance(self):
        """
        The function updates the balance of a user's wallet in a MySQL database.
        
        :param user_id: The user ID is a unique identifier for a specific user in the database. It is used
        to identify which user's wallet balance needs to be updated
        :param balance: The new balance that you want to update for the user's wallet
        """
        try:
            conn = connection()
            
            update_query = "UPDATE wallet SET balance = %s WHERE user_id = %s"
            cursor = conn.cursor()
            cursor.execute(update_query, (self.balance, self.user_id,))
            conn.commit()
        except Error as e:
          print('An exception occurred', e)
          
    def update_address(self):
        """
        The function updates the wallet address of a user in a MySQL database.
        
        :param user_id: The user ID is a unique identifier for a specific user in the database. It is used
        to identify which user's wallet address needs to be updated
        :param address: The new wallet address that needs to be updated in the database
        """
        try:
            conn = connection()
            
            update_query = "UPDATE wallet SET address = %s WHERE user_id = %s"
            cursor = conn.cursor()
            cursor.execute(update_query, (self.address, self.user_id,))
            conn.commit()
        except Error as e:
          print('An exception occurred', e)     