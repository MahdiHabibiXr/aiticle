import psycopg2
from psycopg2 import sql

# conn_params = {
#     'dbname': 'aiticle',
#     'user': 'postgres',
#     'password': 'Y4z#inab',
#     'host': 'localhost',  # e.g., 'localhost'
#     'port': '5432'   # e.g., '5432'
# }

conn_params = {
    'dbname': 'studaio1_aiticle',
    'user': 'studaio1',
    'password': 'hMOz==@d)*$#',
    'host': 'localhost',  # e.g., 'localhost'
    'port': '5432'   # e.g., '5432'
}

def add_user(t_id, ref_id=''):
    try:
        t_id = str(t_id)
        # Connect to your PostgreSQL database
        conn = psycopg2.connect(**conn_params)
        # Create a cursor object
        cursor = conn.cursor()

        # Define the insert query and data
        insert_query = """
        INSERT INTO users (t_id, ref_id)
        VALUES (%s, %s);
        """
        data_to_insert = (t_id, ref_id)

        # Execute the insert query
        cursor.execute(insert_query, data_to_insert)

        # Commit the transaction
        conn.commit()

        print("Data inserted successfully")

        # Remember to close the cursor and connection
        cursor.close()
        conn.close()
        print("PostgreSQL connection is closed")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

def add_request(req_id, t_id):
    try:
        t_id = str(t_id)
        # Connect to your PostgreSQL database
        conn = psycopg2.connect(**conn_params)
        # Create a cursor object
        cursor = conn.cursor()

        # Define the insert query and data
        insert_query = """
        INSERT INTO requests (req_id, t_id)
        VALUES (%s, %s);
        """
        data_to_insert = (req_id, t_id)

        # Execute the insert query
        cursor.execute(insert_query, data_to_insert)

        # Commit the transaction
        conn.commit()

        print("Data inserted successfully")

        # Remember to close the cursor and connection
        cursor.close()
        conn.close()
        print("PostgreSQL connection is closed")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

def get_user(t_id):
    try:
        t_id = str(t_id)
        # Connect to your PostgreSQL database
        conn = psycopg2.connect(**conn_params)
        # Create a cursor object
        cursor = conn.cursor()

        # Define the select query
        select_query = "SELECT * FROM users WHERE t_id = %s;"

        # Execute the select query
        cursor.execute(select_query, (t_id,))

        # Fetch all the records
        records = cursor.fetchall()

        # Print the records
        for row in records:
            print(row)

        # Remember to close the cursor and connection
        cursor.close()
        conn.close()
        print("PostgreSQL connection is closed")

        return records[0]

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

def get_request(req_id):
    try:
    # Connect to your PostgreSQL database
        conn = psycopg2.connect(**conn_params)
        # Create a cursor object
        cursor = conn.cursor()

        # Define the select query
        select_query = "SELECT * FROM requests WHERE req_id = %s;"

        # Execute the select query
        cursor.execute(select_query, (req_id,))

        # Fetch all the records
        records = cursor.fetchall()

        # Print the records
        for row in records:
            print(row)

        # Remember to close the cursor and connection
        cursor.close()
        conn.close()
        print("PostgreSQL connection is closed")

        return records[0]

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

def update_user(t_id, column_name, value):
    try:
        t_id = str(t_id)
        # Connect to your PostgreSQL database
        conn = psycopg2.connect(**conn_params)
        # Create a cursor object
        cursor = conn.cursor()

        # Construct the SQL query dynamically
        query = f"UPDATE users SET {column_name} = %s WHERE t_id = %s"

        # Execute the query with the provided value and t_id
        cursor.execute(query, (value, t_id))

        # Commit the transaction
        conn.commit()

        print(f"Value '{value}' added to column '{column_name}' in table 'users' for t_id '{t_id}'")

        # Close the cursor and connection
        cursor.close()
        conn.close()

    except (Exception, psycopg2.Error) as error:
        print(f"Error while connecting to PostgreSQL: {error}")

def update_request(req_id, column_name, value):
    try:
        # Connect to your PostgreSQL database
        conn = psycopg2.connect(**conn_params)
        # Create a cursor object
        cursor = conn.cursor()

        # Construct the SQL query dynamically
        query = f"UPDATE requests SET {column_name} = %s WHERE req_id = %s"

        # Execute the query with the provided value and t_id
        cursor.execute(query, (value, req_id))

        # Commit the transaction
        conn.commit()

        print(f"Value '{value}' added to column '{column_name}' in table 'requests' for req_id '{req_id}'")

        # Close the cursor and connection
        cursor.close()
        conn.close()

    except (Exception, psycopg2.Error) as error:
        print(f"Error while connecting to PostgreSQL: {error}")

def null(t_id, column_name, conn_params):
    try:
        t_id = str(t_id)
        table_name = 'users'
        # Connect to your PostgreSQL database
        conn = psycopg2.connect(**conn_params)
        # Create a cursor object
        cursor = conn.cursor()

        # Construct the SQL query dynamically
        query = f"UPDATE {table_name} SET {column_name} = NULL WHERE t_id = %s"

        # Execute the query with the provided t_id
        cursor.execute(query, (t_id,))

        # Commit the transaction
        conn.commit()

        print(f"Column '{column_name}' set to NULL in table '{table_name}' for t_id '{t_id}'")

        # Close the cursor and connection
        cursor.close()
        conn.close()

    except (Exception, psycopg2.Error) as error:
        print(f"Error while connecting to PostgreSQL: {error}")

def user_exists(t_id):
    try:
        t_id = str(t_id)
        # Connect to your PostgreSQL database
        conn = psycopg2.connect(**conn_params)
        # Create a cursor object
        cursor = conn.cursor()

        # SQL query to check if the user exists
        query = """
        SELECT 1
        FROM users
        WHERE t_id = %s;
        """

        # Execute the query
        cursor.execute(query, (t_id,))

        # Fetch one result
        user_exists = cursor.fetchone() is not None

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return user_exists

    except (Exception, psycopg2.Error) as error:
        print(f"Error while connecting to PostgreSQL: {error}")
        return False


# add_user('274859', 'img/ai/im.png', '123456', 0)
# get_user('274859')