from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
from dotenv import load_dotenv
import os
load_dotenv()


from config import config

app = Flask(__name__)
cors = CORS(app)



HOST = os.getenv("HOST")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
DB = os.getenv("DB")
# Config MySQL
app.config['MYSQL_HOST'] = HOST
app.config['MYSQL_USER'] = USER
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_PASSWORD'] = PASSWORD
app.config['MYSQL_DB'] = DB
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

conexion = MySQL(app)

@app.route('/')
def list_products():
    cursor=conexion.connection.cursor()
    sql = "SELECT id, name, url_image, price, discount, category FROM product"
    cursor.execute(sql)
    datos=cursor.fetchall()
    dic = {'message': "Success", 'products':datos}
    return jsonify(dic)
    
@app.route('/categories/getbycategory', methods = ['POST'])
def get_products_by_category():
    body = request.get_json()
    cursor = conexion.connection.cursor()
    if "category" in body:
        sql = f"SELECT id FROM category WHERE name = '{body['category']}'"
        cursor.execute(sql)
        id_dic = cursor.fetchone()
        if id_dic:
            id = id_dic['id']
            sql = f"SELECT id, name, url_image, price, discount, category FROM product WHERE category = '{id}'"
            cursor.execute(sql)
            datos = cursor.fetchall()
            dic = {'message': "Success", 'products':datos}
        else:
            dic = {'message':"category not found"}
        return jsonify(dic)
        
    else: 
        return "you must specify a category"

@app.route('/search', methods = ['POST']) 
def search():
    map = {"bebida energetica": 1, "pisco": 2, "ron": 3, "bebida": 4, "snack":5, "cerveza":6, "vodka":7, "todos": "category"}
    body = request.get_json()  
    category = map[body['category']]
    cursor = conexion.connection.cursor()
    sql = "SELECT name FROM category"
    cursor.execute(sql)
    datos = cursor.fetchall()
    print(datos)
    if "search" in body:
        sql = f"SELECT id, name, url_image, price, discount, category FROM product WHERE name LIKE '%{body['search']}%' AND category = {category}"
        cursor.execute(sql)
        datos = cursor.fetchall()
        if not datos:
            return jsonify({'message': "0 Results", 'products':[]})
        dic = {'messagge': "Success", 'products': datos}
    else:
        dic = {'message': "you must specify a search string"}
    return jsonify(dic)

def page_not_found(error):
    return "<h1>The page that you're looking for was not found ...</h1>"

if __name__ == '__main__':
    app.config.from_object(config['development'])    
    app.register_error_handler(404, page_not_found) 
    app.run(debug=True)