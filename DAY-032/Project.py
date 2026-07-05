# PROJECT

# Design an E-Commerce Database schema (users, products, orders, order_items)

# USERS -> id, name, email, password, phone
# PRODUCTS -> id, name, price, stock, category
# ORDERS -> id, user_id, order_date, status, total_price
# ORDER_ITEMS -> id, order_id, product_id, quantity, price

# Relationship
# Users -> Orders -> Order Items -> Products


# Backend Connection:
# Frontend -> FastAPI -> SQLAlchemy -> PostgreSQL
# Every API endpoint will eventually read from or write to tables like these.