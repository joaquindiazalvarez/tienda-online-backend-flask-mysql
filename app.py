from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
import json

from config import config

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'mdb-test.c6vunyturrl6.us-west-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'bsale_test'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_PASSWORD'] = 'bsale_test'
app.config['MYSQL_DB'] = 'bsale_test'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

conexion = MySQL(app)

@app.route('/')
def list_products():
    try:
        cursor=conexion.connection.cursor()
        sql = "SELECT id, name, url_image, price, discount, category FROM product"
        cursor.execute(sql)
        datos=cursor.fetchall()
        print(datos)
        return "products listed"
    except Exception as ex:
        return json.dumps(ex)
@app.route('/categories/getbycategory', methods = ['POST'])
def get_products_by_category():
    body = request.get_json()
    cursor=conexion.connection.cursor()
    if body['category']:
        sql = f"SELECT id FROM category WHERE name = '{body['category']}'"
        cursor.execute(sql)
        idtuple = cursor.fetchone()
        if idtuple:
            id = idtuple[0]
            #print(id)
            sql = f"SELECT id, name, url_image, price, discount, category FROM product WHERE category = '{id}'"
            cursor.execute(sql)
            datos = cursor.fetchall()
            dic = {'message': "Sucess", 'products':[]}
            for element in datos:
                d = {'id':element[0], 'name':element[1], 'url_image':element[2], 'price':element[3], 'discount':element[4], 'category':element[5]}
                dic['products'].append(d)
            print(dic)
        else:
            dic = {'message':"Category not found"}
        return jsonify(dic)
        
    else: 
        return "you must specify a category"

""" @app.route('/getbyid/<int:id>', methods = ['GET'])
def get_product_by_index(id):
    cursor = conexion.connection.cursor()
    sql = f"SELECT id, name, url_image, price, discount, category FROM product WHERE id = '{id}'"
    cursor.execute(sql)
    dato = cursor.fetchone()
    if dato is None:
        return "Product not found"
    dic = {'id': dato[0], 'name': dato[1], 'url_image': dato[2], 'price': dato[3], 'discount': dato[4], 'category': dato[5]}
    return jsonify(dic) """
    


        

def page_not_found(error):
    return "<h1>The page that you're looking for was not found ...</h1>"

if __name__ == '__main__':
    app.config.from_object(config['development'])    
    app.register_error_handler(404, page_not_found) 
    app.run()