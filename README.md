# ⚡API tienda online
## Sobre este proyecto...
Este es un proyecto, el cual está dividido en frontend y backend  
Este repositorio pertenece a la parte del backend (API REST)
## Descripción...
Básicammente lo que hace es conectarse a una base de datos para buscar información y entragarla a través de métodos HTTP(GET y POST)  
La información que maneja es una lista de productos, que tienen nombre, una imágen, un precio, un descuento y una categoría  
# Empezando...
Para correr la aplicación, después de clonar el repositorio, se debe entrar a la carpeta del proyecto con:  
### $ cd tienda-online-backend-flask-mysql
luego se debe crear un virtual enviroment idealmente con:  
### $ virtualenv -p python env  
luego acceter al entorno virtual con:   
### $ source ./env/Scripts/activate  
luego instalar los paquetes necesarios con:  
### $ pip install -r requirements.txt  
y finalmente se puede correr la app con:  
## $ python app.py
# La API
## ⚡Descripción...
Para construir la api se utilizó:
- Flask 
- flask_mysqldb para la conexión con sql
- flask_cors para encargarse del CORS
- dotenv para poder utilizar variables de enviroment
La API se conecta a una base de datos MySQL externa utilizando variables de enviroment, para no revelar las credenciales de la db.  
La API posee 4 endpoints
## Endpoints
- 1: say_hello -> método GET    
![api11](https://imagizer.imageshack.com/img922/7638/Ik71uN.png)  
simplemente saluda:  
![api12](https://imagizer.imageshack.com/img922/2815/HtjgI4.png)
- 2: list_products -> método GET  
![api21](https://imagizer.imageshack.com/img922/9880/h8uxYC.png)
trae todos los productos en la db:  
![api22](https://imagizer.imageshack.com/img924/1746/lx2D85.png)  
- 3: get_products_by_category -> método POST  
![api31](https://imagizer.imageshack.com/img924/6461/aG98mi.png)  
Este endpoint requiere de un parámetro enviado a través de la url, que indica la página que se quiere traer de la query   
También requiere tres parámetros captados a través de JSON, los cuales son:  
- category -> string de la categoría que debe tener el producto  
- order -> string de orden en que se quiere listar el producto, puede ser de la A a la Z, de la Z a la A, Menor precio y Mayor precio  
- discount -> boolean que indica si solo se requieren productos con descuento  
![api321](https://imagizer.imageshack.com/img923/3021/Rdohes.png)  
la api nos retorna una objeto con un mensaje, el número de página y un array con los productos  
![api322](https://imagizer.imageshack.com/img923/2210/DwIF4V.png)  