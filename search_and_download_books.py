import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import boto3
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configuración de AWS S3
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

# Inicializar el navegador
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

def search_books():
    driver.get('https://openlibrary.org/')

    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys('Julio Verne')
    search_box.send_keys(Keys.RETURN)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, 'Authors'))
    )
    author_filter = driver.find_element(By.LINK_TEXT, 'Authors')
    author_filter.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.authorName'))
    )
    verne_link = driver.find_element(By.LINK_TEXT, 'Jules Verne')
    verne_link.click()

def download_top_books():
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.searchResultItem'))
    )
    books = driver.find_elements(By.CSS_SELECTOR, '.searchResultItem')

    top_books = books[:3]  # Obtener los 3 primeros libros

    for i, book in enumerate(top_books):
        title = book.find_element(By.CSS_SELECTOR, '.bookTitle').text
        book_url = book.find_element(By.CSS_SELECTOR, '.bookTitle').get_attribute('href')

        driver.get(book_url)

        try:
            download_link = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, 'Download'))
            )
            download_url = download_link.get_attribute('href')
            response = requests.get(download_url)
            file_name = f'book_{i + 1}.pdf'
            with open(file_name, 'wb') as file:
                file.write(response.content)

            # Subir a S3
            s3.upload_file(file_name, BUCKET_NAME, file_name)
            print(f'{file_name} subido a S3.')

        except Exception as e:
            print(f'Error al descargar el libro: {e}')

def lambda_handler(event, context):
    search_books()
    download_top_books()
    driver.quit()
    return {
        'statusCode': 200,
        'body': 'Libros descargados y subidos a S3.'
    }

if __name__ == '__main__':
    search_books()
    download_top_books()
    driver.quit()
