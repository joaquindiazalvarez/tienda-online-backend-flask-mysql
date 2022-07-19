from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
from dotenv import load_dotenv
import os
load_dotenv()
#se cargen las variables de enviroment

"""
###INSTRUCCIONES###
cursor=conexion.connection.cursor()
#permite al código de python ejecutar un comando en la sesión de la db

cursor.execute(sql)
#ejecuta la query en la db

data=cursor.fetchall()
#guarda el resultado de la query a la db en una variable
###
"""


app = Flask(__name__)
#se crea una instancia del objeto Flask(se crea la aplicación)
cors = CORS(app)
#esta instancia se encarga del CORS

HOST = os.getenv("HOST")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
DB = os.getenv("DB")
#se setean las variables de enviroment

app.config['MYSQL_HOST'] = HOST
app.config['MYSQL_USER'] = USER
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_PASSWORD'] = PASSWORD
app.config['MYSQL_DB'] = DB
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
#se configura la conexión a la base de datos

conexion = MySQL(app)
#se establece la conexión de Flask con la base de datos

@app.route('/')
def say_hello():
    """
    Endpoint de ejemplo
    args: ninguno
    retorna: un saludo
    """
    return '<h1>Hello World, this is my online-store API</h1>'

@app.route('/getall', methods = ['GET'])
def list_products():
    """
    Endpoint para traer todos los productos
    args: ninguno
    return: un JSON con todos los productos
    """
    cursor=conexion.connection.cursor()
    sql = "SELECT id, name, url_image, price, discount, category FROM product"
    cursor.execute(sql)
    data=cursor.fetchall()
    dic = {'message': "Success", 'products':data}
    return jsonify(dic)
    
@app.route('/categories/getbycategory/<int:page>/', methods = ['POST'])
def get_products_by_category(page):
    """
    Endpoint para traer productos que tengan la categoría señalada
    args:
        ruta:
            page, indica la página que desea traerse
        body:
            category, se traen solo los productos con la categoría indicada
            discount, si es True, se traen solo los productos con descuento
            order, se ordenan los productos según order
    return: JSON con productos con la categoría señalada, ordenados y paginados
    """
    body = request.get_json()
    page_limit = 12
    #se setea cuantos productos irán por página
    cursor = conexion.connection.cursor()
    if "discount" in body:
        if body['discount'] == True:
            discount = "AND discount > '0'"
            discount_where = "WHERE discount > '0'"
        else: 
            discount = ""
            discount_where = ""
    #sentencias que se agregan a la query para filtrar por descuento
    else:
        dic = {'message': "must specify discount"}
        return jsonify(dic)
    if "category" in body and "order" in body:
        if body['order'] == "az":
            parameter = "name"
            order = "ASC"
        elif body['order'] == "za":
            parameter = "name"
            order = "DESC"
        elif body['order'] == "pricemin":
            parameter = "price"
            order = "ASC"
        elif body['order'] == "pricemay":
            parameter = "price"
            order = "DESC"
        #se setean el template para ordenar la query
        if body['category'] == "todos":
            #en este caso la categoría es todos. Se traen todos los productos que cumplan con el orden, la paginación y el descuento
            sql = f"SELECT id, name, url_image, price, discount, category FROM product {discount_where} ORDER BY {parameter} {order}"
            cursor.execute(sql)
            data = cursor.fetchall()
            first_element = (page - 1)* page_limit
            last_element = (page * page_limit)
            #se calcula cual debe ser el primer y ultimo elemento de la página
            data_cut = data[first_element:last_element]
            #se toma la parte del arreglo que corresponde a la paginación
            dic = {'message': "Success", 'products': data_cut, 'pages': len(data)//page_limit + 1, 'products_length':len(data)}
            if page < 1 or page > dic['pages']:
                dic = {'message': "Page out of range"}
                return jsonify(dic)
            return jsonify(dic)
        sql = f"SELECT id FROM category WHERE name = '{body['category']}'"
        #si no se cumple que la categoría sea todos, se ejecuta otra query
        #que convierte el string de categoría en un id
        cursor.execute(sql)
        id_dic = cursor.fetchone()
        if id_dic:
            id = id_dic['id']
            sql = f"SELECT id, name, url_image, price, discount, category FROM product WHERE category = '{id}' {discount} ORDER BY {parameter} {order}"
            cursor.execute(sql)
            data = cursor.fetchall()
            first_element = (page - 1)* page_limit
            last_element = (page * page_limit)
            #se calcula cual debe ser el primer y último elemento de la página
            data_cut = data[first_element:last_element]
            #se toma la parte del arreglo que corresponde a la paginación
            dic = {'message': "Success", 'products': data_cut, 'pages':len(data)//page_limit + 1, 'products_length':len(data)}
            if page < 1 or page > dic['pages']:
                dic = {'message': "Page out of range"}
                return jsonify(dic)
            return jsonify(dic)
        else:
            dic = {'message':"category not found"}
        return jsonify(dic)
        
    else: 
        dic = {'message': "you must specify a category and an order"}
        return jsonify(dic)

@app.route('/search/<int:page>/', methods = ['POST']) 
def search(page):
    """
    Endpoint para traer productos que tengan la categoría señalada
    args:
        ruta:
            page, indica la página que desea traerse
        body:
            search, se traen los productos que contengan este string en el nombre
            discount, si es True, se traen solo los productos con descuento
            order, se ordenan los productos según order
    return: JSON con productos con la búsqueda señalada, ordenados y paginados
    """
    page_limit = 12
    #se setea cuantos productos irán por página
    map = {"bebida energetica": 1, "pisco": 2, "ron": 3, "bebida": 4, "snack":5, "cerveza":6, "vodka":7, "todos": "category"}
    body = request.get_json()  
    category = map[body['category']]
    if "discount" in body:
        if body['discount'] == True:
            discount = "AND discount > '0'"
        else: 
            discount = ""
    #sentencias que se agregan a la query para filtrar por descuento
    else:
        dic = {'message': "must specify discount"}
        return jsonify(dic)
    if category:
        cursor = conexion.connection.cursor()
        if "search" in body and "order" in body:
            if body['order'] == "az":
                parameter = "name"
                order = "ASC"
            elif body['order'] == "za":
                parameter = "name"
                order = "DESC"
            elif body['order'] == "pricemin":
                parameter = "price"
                order = "ASC"
            elif body['order'] == "pricemay":
                parameter = "price"
                order = "DESC"
            #se setean el template para ordenar la query
            sql = f"SELECT id, name, url_image, price, discount, category FROM product WHERE name LIKE '%{body['search']}%' AND category = {category} {discount} ORDER BY {parameter} {order}"
            cursor.execute(sql)
            data = cursor.fetchall()
            if not data:
                return jsonify({'message': "0 Results", 'products':[]})
            first_element = (page - 1)* page_limit
            last_element = (page * page_limit)
            #se calcula cual debe ser el primer y ultimo elemento de la página
            data_cut = data[first_element:last_element]
            #se toma la parte del arreglo que corresponde a la paginación
            dic = {'messagge': "Success", 'products': data_cut, 'pages':len(data)//page_limit + 1, 'products_length':len(data)}
            if page < 1 or page > dic['pages']:
                dic = {'message': "Page out of range"}
                return jsonify(dic)
            return jsonify(dic)
        else:
            dic = {'message': "you must specify a search stringand an order"}
    else:
        dic = {'message': "you must specify a category"}
    return jsonify(dic)

def page_not_found(error):
    """
    función que capta las rutas que no están definidas
    return: mensaje
    """
    return "<h1>The page that you're looking for was not found ...</h1>"

if __name__ == '__main__': 
    app.register_error_handler(404, page_not_found) 
    app.run()
    #corre la aplicación