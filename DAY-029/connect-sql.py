import psycopg

conn = psycopg.connect(
    host="localhost",
    dbname="backend_journey",
    user="postgres",
    password="inside .env",
    port=5432
)

print("Connected Successfully!")

conn.close()