from connection import connection

def execute_query(query, params=None):
    """
    Executes the given SQL query on the MySQL database.
    
    :param query: The SQL query to execute.
    :param params: Optional parameter that contains any variables that are used in the SQL query.
    :return: The result of the query, as returned by the MySQL database.
    """
    conn = connection()
    cursor = conn.cursor()   
     
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    
    result = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return result

def execute_multiple_query(query, params=None):
    """
    Executes the given SQL query on the MySQL database.
    
    :param query: The SQL query to execute.
    :param params: Optional parameter that contains any variables that are used in the SQL query.
    :return: The result of the query, as returned by the MySQL database.
    """
    conn = connection()
    cursor = conn.cursor()   
     
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result