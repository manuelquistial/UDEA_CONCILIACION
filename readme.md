## Conciliacion
Este es un monolito desarrollado en <a href="https://laravel.com/docs/5.5">Laravel v5.5</a> y conserva la estructura propuesta por la documentacion.<br>
**Para la conciliacion se requiere conocimientos de PYTHON y Pandas.**<br>
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
   - PYTHON

## Nombre de archivos para conciliacion<br>
Los documentos a subir para conciliar son
- General_SIGEP_{centro_costos}.xlsx
- Pagos_SAP_{centro_costos}.xlsx
- Recaudos_SAP_{centro_costos}.xlsx

## Requerimientos

- PHP v7.0.22
- LARAVEL v5.5
- COMPOSER v
- PYTHON 3.8

## Instalacion

1. Instalar paquetes del repositorio
```
php7 composer install
```

2. Crear carpeta *conciliacion* para almacenar los documentos a conciliar
```
mkdir storage/app/public/conciliacion
```
3. Crear carpeta *files_out* para almacenar la conciliacion
```
mkdir storage/app/public/files_out
```

3. Permiso *775* a folders *bootstrap* y *storage*
```
chown {user}:www-data storage/app/public/{folder} -R
chmod 775 storage/ -R
```

3. Configurar *.env*
  - Copiar *.env*
    ```
    cp .env.example .env
    ```
  - Nombrar aplicacion en *APP_NAME*, ej: "Conciliacion - Facultad de Comunicaciones"
  - Definir *APP_ENV* como "local" para desarrollo o "production" para produccion
  - Definir *APP_DEBUG* como "false" para produccion o "true" para desarrollo
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
4. Instalar paquetes de python
```
pip install -r requirements.txt
```
## Base de datos
**Solo ejecutar este paso en caso de crear desde cero la aplicacion.**<br>
**La DB de Conciliacion se almacena en la misma DB de SITA.**<br>
Con este comando se crean desde cero todas las tablas de la aplicacion.
```
php7 artisan migrate
```
