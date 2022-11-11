from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/products', methods=['GET'])
def getProducts():
    # connecting to the database
    dataBase = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="jkvlEdsvn1254!!!",
        database="store")
    # preparing a cursor object
    cursorObject = dataBase.cursor()
    # SQL queries
    select_data_query = """with a as
                           (SELECT p.product_name, c.category_name
                           FROM product AS p
                           LEFT JOIN product_category AS pc ON p.product_id = pc.product_id
                           LEFT JOIN category         AS c  ON pc.category_id = c.category_id
                           UNION
                           SELECT p.product_name, c.category_name
                           FROM product AS p
                           RIGHT JOIN product_category AS pc ON p.product_id = pc.product_id
                           RIGHT JOIN category         AS c  ON pc.category_id = c.category_id)
                           SELECT a.product_name, GROUP_CONCAT(a.category_name SEPARATOR ', ') 
                           from a
                           GROUP BY a.product_name
                        """
    # display data from SQL queries
    cursorObject.execute(select_data_query)
    result = cursorObject.fetchall()
    # disconnecting from server
    dataBase.close()
    return result

@app.route('/categories', methods=['GET'])
def getCategories():
    # connecting to the database
    dataBase = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="jkvlEdsvn1254!!!",
        database="store")
    # preparing a cursor object
    cursorObject = dataBase.cursor()
    # SQL queries
    select_data_query = """with a as
                           (SELECT p.product_name, c.category_name
                           FROM product AS p
                           LEFT JOIN product_category AS pc ON p.product_id = pc.product_id
                           LEFT JOIN category         AS c  ON pc.category_id = c.category_id
                           UNION
                           SELECT p.product_name, c.category_name
                           FROM product AS p
                           RIGHT JOIN product_category AS pc ON p.product_id = pc.product_id
                           RIGHT JOIN category         AS c  ON pc.category_id = c.category_id)
                           SELECT GROUP_CONCAT(a.product_name SEPARATOR ', '), a.category_name 
                           from a
                           GROUP BY a.category_name
                        """
     # display data from SQL queries
    cursorObject.execute(select_data_query)
    result = cursorObject.fetchall()
    # disconnecting from server
    dataBase.close()
    return result

@app.route('/pairProductCategory', methods=['GET'])
def getPairsProductCategory():
    # connecting to the database
    dataBase = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="jkvlEdsvn1254!!!",
        database="store")
    # preparing a cursor object
    cursorObject = dataBase.cursor()
    # SQL queries
    select_data_query = """with a as
                           (SELECT p.product_name, c.category_name
                           FROM product AS p
                           LEFT JOIN product_category AS pc ON p.product_id = pc.product_id
                           LEFT JOIN category         AS c  ON pc.category_id = c.category_id
                           UNION
                           SELECT p.product_name, c.category_name
                           FROM product AS p
                           RIGHT JOIN product_category AS pc ON p.product_id = pc.product_id
                           RIGHT JOIN category         AS c  ON pc.category_id = c.category_id)
                           SELECT a.product_name, a.category_name 
                           from a
                        """
    # display data from SQL queries
    cursorObject.execute(select_data_query)
    result = cursorObject.fetchall()
    # disconnecting from server
    dataBase.close()
    return result

if __name__ == '__main__':
    app.run()
    # SQL database dump is in store.sql file
    # prints "Hello, World!" in https://http://127.0.0.1:5000/
    # prints list of products in https://http://127.0.0.1:5000/products/
    # prints list of categories in https://http://127.0.0.1:5000/categories/
    # prints pairs product-category in https://http://127.0.0.1:5000/pairProductCategory/