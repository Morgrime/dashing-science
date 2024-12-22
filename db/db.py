# import psycopg2
# from config.config import DB_PASS, DB_HOST, DB_NAME, DB_PORT, DB_USER

# conn = psycopg2.connect(conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, 
#                                                 password=DB_PASS, host=DB_HOST,
#                                                 ))

# cursor = conn.cursor()

# def create_table():
#     cur = cursor()
#     cur.execute("""
#     CREATE TABLE IF NOT EXISTS orders (
#                 id SERIAL PRIMARY KEY,
#                 service VARCHAR (15) NOT NULL,
#                 originality VARCHAR (5) NOT NULL,
#                 deadline INT NOT NULL,
#                 wishes VARCHAR (500),
#                 cost INT)
#     """)
#     cur.commit()
#     cur.close()

# def select_all():
#     cur = cursor()
#     cur.execute("""
#     SELECT * FROM orders
#     """)


# def add_order(service, originality, deadline, wishes, cost):
#     cur = cursor()
#     cur.execute(f"""
#     INSERT INTO orders ()
#     """)