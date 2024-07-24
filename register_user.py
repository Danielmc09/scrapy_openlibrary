import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Inicializar el navegador
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

def register_user():
    driver.get('https://openlibrary.org/account/create')

    username = driver.find_element(By.ID, 'username')
    email = driver.find_element(By.ID, 'email')
    password = driver.find_element(By.ID, 'password')
    password_confirm = driver.find_element(By.ID, 'password_confirm')

    username.send_keys('your_username')
    email.send_keys('your_email@example.com')
    password.send_keys('your_password')
    password_confirm.send_keys('your_password')
    password_confirm.send_keys(Keys.RETURN)

    try:
        success_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.flash .flash-success'))
        )
        print('Registro exitoso')
    except Exception as e:
        print(f'Error al registrarse: {e}')

def lambda_handler(event, context):
    register_user()
    driver.quit()
    return {
        'statusCode': 200,
        'body': 'Usuario registrado exitosamente.'
    }

if __name__ == '__main__':
    register_user()
    driver.quit()
