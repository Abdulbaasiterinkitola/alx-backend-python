#!/usr/bin/python3
import seed

def stream_users():
    """Generator yielding users one by one."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    for row in cursor:   # only one loop allowed
        yield row

    cursor.close()
    connection.close()