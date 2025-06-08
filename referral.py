from execute_query import execute_query
from execute_query import execute_multiple_query
from connection import connection
from mysql.connector import Error

class Referral:
    def __init__(self, user_id, input_link=None, referrer_id=None, referral_count=None, referral_balance=None):
        self.user_id = user_id
        self.input_link = input_link
        self.referrer_id = referrer_id
        self.referral_count = referral_count
        self.referral_balance = referral_balance
                        
    def has_link(self):
        """
        Checks if a referral link exists for a given user ID in the MySQL database.
        """
        link = None  # Initialize link
        try:
            count_query = "SELECT COUNT(*) FROM referral_link WHERE user_id = %s"
            count_result = execute_query(count_query, (self.user_id,))
            count = True if count_result > 0 else False
            
            if count is True:
                link_query = "SELECT referred_link FROM referral_link WHERE user_id = %s"
                link_result = execute_query(link_query, (self.user_id,))
                link = link_result
            else:
                return None, False
            
            return link, True
        except Error as e:
            print('An exception occurred', {e})
        
        return None, False
    
    def add_link(self):
        try:  
            conn = connection()        
            insert_query = """
                INSERT INTO referral_link (user_id, referred_link) 
                VALUES (%s, %s)
                """
            values = (self.user_id, self.input_link)
            
            with conn.cursor() as cursor:
                cursor.execute(insert_query, values)
            conn.commit()
                        
        except Error as e:
            print(f"Database error occurred: {e}")
    
    def add_referrer_data(self):
        """
        Populates referral data for a user.
        """
        try:  
            conn = connection()        
            insert_query = """
                INSERT INTO referral_data (user_id, referrer_id, referral_count, referral_balance) 
                VALUES (%s, %s, %s, %s)
                """
            values = (self.user_id, self.referrer_id, 0, 0)
            
            with conn.cursor() as cursor:
                cursor.execute(insert_query, values)
            conn.commit()
                        
        except Error as e:
            print(f"Database error occurred: {e}")

    def referrer_data(self):
        """
        The function retrieves the referral count for a given user ID from a MySQL database.
        
        :param user_id: The user ID is a unique identifier for a specific user in the referral_data table.
        It is used to retrieve the referral count for that particular user
        :return: the referral count of a user with the given user_id from the referral_data table in the
        bot database.
        """
        try:
            select_query = "SELECT referrer_id, referral_count, referral_balance FROM referral_data WHERE user_id = %s"
            result = execute_multiple_query(select_query, (self.user_id,))
            if result:
                return result
            else:
                return (0,0,0)
        except Error as e:
            print(f"Database error occurred: {e}")
            return (None, None, None)  # Return a tuple indicating failure
    
    def increment(self):
        """
        This function updates the referral count of a user in a MySQL database.
        
        :param user_id: The user ID is a unique identifier for a specific user in the referral_data table.
        It is used to identify which user's referral count needs to be updated
        :param referral_count: The number of referrals that the user has made
        """
        try:
            conn = connection()
            update_query = "UPDATE referral_data SET referral_count = %s, referral_balance = %s WHERE user_id = %s"
            cursor = conn.cursor()
            cursor.execute(update_query, (self.referral_count, self.referral_balance, self.user_id,))
            conn.commit()
        except Error as e:
          print('An exception occurred', {e})
            