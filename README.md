# Business Reviews

Aplicación web para la reseña de negocios (tipo Yelp o Foursqaure City Guide) utilizada en  procesos de enseñanza-aprendizaje. La aplicación está desarrollada sobre el microframework [Flask](https://flask.palletsprojects.com/) y hace uso de otros servicios.

## Entorno de desarrollo local

El proyecto se ha probado con Python 3.8 y la herramienta [Poetry](https://python-poetry.org/) para la gestión de paquetes, dependencias y entornos virtuales.

Instala Poetry en el equipo según las [instrucciones de la documentación oficial](https://python-poetry.org/docs/#installation).

La instalación de las dependencias también creará un entorno virtual para el proyecto. Si se desea que este entorno virtual se encuentre en el propio proyecto, se deberá crear un directorio llamado `.venv` en la raíz del proyecto antes de instalar las dependencias.

```bash
$ mkdir .venv ### Opcional
$ poetry install
$ poetry install --no-dev ### No instala las dependencias de desarrollo
```

Para activar el entorno virtual del proyecto puedes ejecutar `poetry shell`.

## Persistencia base de datos

Se puede utilizar una base de datos MySQL/MariaDB, PostgreSQL o SQLite. En los dos primeros casos, habrá que instalar los paquetes extra que habiliten la conexión.

```bash
$ poetry install -E mysql-alt
$ poetry install -E mysql ### Necesita el CLI de mysql-client instalado en el equipo
$ poetry install -E pgsql-alt
$ poetry install -E pgsql ### Necesita el CLI, un compilador C y las cabeceras de Python y libpq instalado en el equipo
```

Por defecto, el proyecto utiliza una base de datos SQLite.

## Ejecución de la aplicación

### Configuración del entorno

Para la configurar la aplicación se necesitan algunas variables de entorno que puedes añadir al fichero `.env`. Si no se definen, toman los valores por defecto según el código del fichero `app/config.py`.

En el fichero .flaskenv se definen las variables de entorno `$FLASK_AP` y `$FLASK-EN`. La variable de entorno `$FLASK_APP` indica el fichero que actuará como punto de entrada para poder lanzar la aplicación. La variable de entorno `$FLASK_ENV` indica el entorno en el que se ejecutará la aplicación (desarrollo o producción).

### Creación de la base de datos

Se debe disponer de un servidor de bases de datos MySQL/MariaDB o PostgreSQL y configurar la variable de entorno `$SQLALCHEMY_DATABASE_URI`. Si no se dispone de ningún servidor de bases de datos o no se ha definido la variable de entorno, se hace uso de SQLite.

Para la configuración inicial de la base de datos se utiliza [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/). El repositorio de migración y la migración inicial ya están creados. Para crear las tablas de la base de datos:

```bash
$ flask db upgrade
```

### Compilación de los paquetes de idiomas

La aplicación está preparada para los idiomas inglés y castellano. Para compilar las traducciones y que el sistema funcione correctamente:

```bash
$ pybabel compile -d app/translations
```

### Otras consideraciones

- La aplicación utiliza Redis como mecanismo de caché. Se debe instalar un servidor Redis y configurar las variables de entorno correspondientes. Si no se encuentra ningún servidor Redis, se encuentra preconfigurado [FakeRedis](https://pypi.org/project/fakeredis/) (para desarrollo o pruebas).
- Se hace uso de la [aplicación web Hashvatar](https://hashvatar.vercel.app/). Puede resultar interesante clonar este servicio para ejecutarlo en el equipo local.

### Por último...

Una vez definidas las variables de entorno y configurados los servicios necesarios, se puede lanzar el el servidor WSGI de desarrollo con el comando

```bash
$ flask run
```

Si no tienes el comando `flask` disponible, puedes ejecutarlo como un módulo Python.

```bash
$ python -m flask run
```
