#!/usr/bin/python3
import seed

def stream_user_ages():
    """Generator yielding ages one by one."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")

    for row in cursor:
        yield row["age"]

    cursor.close()
    connection.close()


def average_age():
    """Calculate average age using streaming."""
    total, count = 0, 0
    for age in stream_user_ages():
        total += age
        count += 1

    if count:
        print(f"Average age of users: {total / count:.2f}")
    else:
        print("No users in database")


if __name__ == "__main__":
    average_age()