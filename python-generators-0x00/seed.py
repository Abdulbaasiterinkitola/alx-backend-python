#!/usr/bin/python3
import mysql.connector
import csv
import uuid

def connect_db():
    """Connect to MySQL server (without database)."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",      # update if needed
            password="root"   # update if needed
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def create_database(connection):
    """Create ALX_prodev if not exists."""
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    cursor.close()


def connect_to_prodev():
    """Connect to ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def create_table(connection):
    """Create user_data table."""
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL
        )
    """)
    connection.commit()
    print("Table user_data created successfully")
    cursor.close()


def insert_data(connection, csv_file):
    """Insert CSV data into user_data."""
    cursor = connection.cursor()
    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            uid = str(uuid.uuid4())
            cursor.execute("""
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE name=VALUES(name), email=VALUES(email), age=VALUES(age)
            """, (uid, row["name"], row["email"], row["age"]))
    connection.commit()
    cursor.close()
