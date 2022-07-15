from flask import Flask
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

def page_not_found(error):
    return "<h1>The page that you're looking for was not found ...</h1>"

if __name__ == '__main__':
    app.config.from_object(config['development'])    
    app.register_error_handler(404, page_not_found) 
    app.run()