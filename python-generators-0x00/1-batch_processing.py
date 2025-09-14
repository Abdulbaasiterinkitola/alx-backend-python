#!/usr/bin/python3
import seed

def stream_users_in_batches(batch_size):
    """Generator yielding batches of users using yield."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield rows   # <-- yield instead of return

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """Filter and print users over 25."""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user["age"] > 25:
                print(user)