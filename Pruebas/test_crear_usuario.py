
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from datetime import datetime

archivo_resultado = "resultados_login.txt"
os.makedirs("screenshots", exist_ok=True)

def guardar_resultado(nombre_prueba, resultado):
    with open(archivo_resultado, "a") as f:
        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{ahora}] {nombre_prueba}: {resultado}\n")
    print(f"{nombre_prueba}: {resultado}")

def capturar_error(driver, nombre_prueba):
    path = f"screenshots/{nombre_prueba.replace(' ', '_')}.png"
    driver.save_screenshot(path)
    print(f"📸 Captura guardada: {path}")

def test_crear_usuario():
    nombre_prueba = "Crear nuevo usuario"
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        driver.get("http://localhost/control/Control/login.php")
        driver.find_element(By.NAME, "user_name").send_keys("admin")
        driver.find_element(By.NAME, "user_password").send_keys("admin", Keys.RETURN)
        time.sleep(2)
        driver.get("http://localhost/control/Control/usuarios.php")
        time.sleep(2)
        nuevo_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Nuevo Usuario')]")))
        nuevo_btn.click()
        time.sleep(1)
        wait.until(EC.visibility_of_element_located((By.ID, "firstname"))).send_keys("Juan")
        driver.find_element(By.ID, "lastname").send_keys("Pérez")
        driver.find_element(By.ID, "user_name").send_keys("japerez")
        driver.find_element(By.ID, "user_email").send_keys("japerez@correo.com")
        driver.find_element(By.ID, "user_password_new").send_keys("123456")
        driver.find_element(By.ID, "user_password_repeat").send_keys("123456")
        driver.find_element(By.XPATH, "//button[contains(text(), 'Guardar datos')]").click()
        time.sleep(2)

        if "jperez" in driver.page_source:
            guardar_resultado(nombre_prueba, "✅ Usuario creado correctamente")
        else:
            guardar_resultado(nombre_prueba, "❌ Usuario no se visualiza en tabla")
            capturar_error(driver, nombre_prueba)

    except Exception as e:
        guardar_resultado(nombre_prueba, f"❌ Error: {e}")
        capturar_error(driver, nombre_prueba)

    driver.quit()

test_crear_usuario()