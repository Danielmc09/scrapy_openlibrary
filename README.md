
# Scrapy openlibrary

Este proyecto permite buscar libros de Julio Verne en Open Library y descargar los 3 más valorados utilizando Selenium, y subirlos a un bucket de S3 en AWS. Además, permite registrarse en Open Library automáticamente usando Selenium. Todo esto se puede ejecutar mediante AWS Lambda.

## Requisitos

- Python 3.x
- AWS CLI configurado
- Selenium
- Boto3
- Requests
- Python-dotenv

## Instalación

1. Clona este repositorio.
2. Crea un entorno virtual y actívalo.
3. Instala las dependencias:

```sh
pip install -r requirements.txt
```

4. Configura tus credenciales de AWS y otros parámetros en un archivo `.env` en el directorio raíz del proyecto:

```env
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_REGION=your_aws_region
S3_BUCKET_NAME=your_s3_bucket_name
```

## Uso

### Buscar y Descargar Libros de Julio Verne

Ejecuta el script `search_and_download_books.py`:

```sh
python search_and_download_books.py
```

### Registrar Usuario en Open Library

Ejecuta el script `register_user.py`:

```sh
python register_user.py
```

## Configuraciones en AWS

1. **Crear un bucket S3**: Ve a la consola de S3 y crea un nuevo bucket.
2. **Configurar AWS Lambda**:
    - Ve a la consola de Lambda y crea nuevas funciones.
    - Selecciona "Author from scratch".
    - Nombres: `search_and_download_books_function` y `register_user_function`.
    - Runtime: Python 3.x.
    - Configura un rol con permisos para acceder a S3 y ejecutar Lambda.
3. **Subir el código de Lambda**:
    - Empaqueta el código Python y las dependencias en un archivo ZIP.
    - Sube el archivo ZIP a la consola de Lambda.
4. **Configurar variables de entorno en Lambda**:
    - Configura las variables de entorno para las credenciales de AWS y el nombre del bucket.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request.

## Licencia

Este proyecto está bajo la Licencia MIT.

Autor: <a href="https://www.linkedin.com/in/danielmendietadeveloper/">Angel Daniel Menideta Castillo</a> © 2024