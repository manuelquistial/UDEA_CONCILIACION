# Conciliacion
Este es un monolito desarrollado en <a href="https://laravel.com/docs/5.5">Laravel v5.5</a> y conserva la estructura propuesta por la documentacion.<br>
**EN PRODUCCION, la base de datos de Conciliacion se almacena en la misma base de datos de SITA.**<br><br>
Conomientos bases para este proyecto<br>
 - Frotend
   - HTML
   - Javascript
   - JQuery
   - CSS, Framework <a href="https://getbootstrap.com/docs/5.2/getting-started/introduction/">Bootstrap</a>
   - REST API
 - Backend
   - PHP
   - Laravel
 - Datos
   - Python
   - Pandas

## Nombre de archivos para conciliacion

Los documentos a subir para conciliar son
- General_SIGEP_{centro_costos}.xlsx
- Pagos_SAP_{centro_costos}.xlsx
- Recaudos_SAP_{centro_costos}.xlsx

## Requerimientos

- PHP v7.0.22
- Composer v1
- Python v3.8

## Instalacion Laravel

- Instalar paquetes del repositorio
```
php composer install
```

- Crear aplicacion key
```
php artisan key:generate
```

- Permiso *775* a folders *bootstrap* y *storage*
```
chown {user}:www-data storage/app/public/{folder} -R
chmod 775 storage/ -R
```

- Configurar *.env*
  - Copiar *.env*
    ```
      cp .env.example .env
    ```
  - Definir *APP_ENV* como *local* para desarrollo o *production* para produccion
  - Definir *APP_DEBUG* como *false* para produccion o *true* para desarrollo
  - Definir en *APP_URL* la URL completa
    - Produccion, ej: "https://comunicaciones.udea.edu.co/conciliacion/index.php"
    - Desarrollo, ej: "http://localhost/UDEA_CONCILIACION/public/index.php"
  - Definir conexion de base de datos
    ```
      DB_CONNECTION=mysql
      DB_HOST=127.0.0.1
      DB_PORT=3306
      DB_DATABASE=homestead
      DB_USERNAME=homestead
      DB_PASSWORD=secret
    ```
  - Definir conexion de correo<br>
    **Recordar que en la Universidad de Antioquia solo se pueden utilizar correos de tipo no-reply.**
    ```
      MAIL_DRIVER=smtp
      MAIL_HOST=smtp.mailtrap.io
      MAIL_PORT=2525
      MAIL_USERNAME=null
      MAIL_PASSWORD=null
      MAIL_ENCRYPTION=null
    ```
## Migrate tablas
**Solo ejecutar este paso en caso de crear la aplicacion desde cero.**<br>
```
php artisan migrate
```

## Populate seed
**Solo ejecutar este paso en caso de crear la aplicacion desde cero.**
```
php artisan db:seed
```

## Instalar paquetes de python

Utilizar `pip` o `pip3` segun este configurado en el sistema

- ``` pip install -r requirements.txt```

## Instalar *pip-compile*

- ```python -m pip install pip-tools```
## Agregar nuevas dependencias

Las dependencias se deben agregar dentro del archivo `requirements.in` y luego ser compiladas, estas se generan en el archivo `requirements.txt`

- ```pip-compile requirements.in```

## Actualizar dependencias

- ```pip-compile --upgrade requirements.in```

## Docker

Crear un contenedor de docker para el proyecto

``` docker-compose up -d  ```

Utilizar *.sh* de la carpeta *docker* para instalar los paquetes con *composer* y utilizar *php artisan*.

- ``` sh ./docker/composer.sh install ```
- ``` sh ./docker/php-artisan.sh migrate ```

### IP docker image
``` docker inspect {image_id} --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ```

