from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

from config import config

app = Flask(__name__)

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
        return "Error"
@app.route('/categories/getbycategory', methods = ['GET'])
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
        return "not ok"

        

def page_not_found(error):
    return "<h1>The page that you're looking for was not found ...</h1>"

if __name__ == '__main__':
    app.config.from_object(config['development'])    
    app.register_error_handler(404, page_not_found) 
    app.run()