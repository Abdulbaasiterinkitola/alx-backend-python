# Python Generators & MySQL Project

This project demonstrates how to use **Python generators** to stream, batch, paginate, and aggregate data from a MySQL database efficiently.  

It is divided into five main tasks:

1. **Task 0:** Database setup and seeding  
2. **Task 1:** Streaming users row by row  
3. **Task 2:** Batch processing with filtering  
4. **Task 3:** Lazy pagination  
5. **Task 4:** Memory-efficient aggregation  

---

## 📌 Prerequisites

- Python 3.x  
- MySQL server (running locally)  
- Python dependencies:
  ```bash
  pip install mysql-connector-python
  ```

# 🚀 Task 0 – Database Setup and Seeding

We first create a database ALX_prodev, a table user_data, and populate it with sample users from user_data.csv.

## Files

- seed.py → helper functions to create DB, table, and insert CSV rows.

- 0-main.py → entry script to test DB setup.

## Steps

1. Ensure MySQL is running locally.

2. Update credentials in seed.py if needed (default is user="root", password="root").

3. Run the main file:
```bash
python3 0-main.py
```
4. Expected Output:
```css
connection successful
Table user_data created successfully
Database ALX_prodev is present
[...]
```