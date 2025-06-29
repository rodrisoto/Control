from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import os

archivo_resultado = "resultados_login.txt"
os.makedirs("screenshots", exist_ok=True)

def guardar_resultado(nombre_prueba, resultado):
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(archivo_resultado, "a") as f:
        f.write(f"[{ahora}] {nombre_prueba}: {resultado}\n")
    print(f"{nombre_prueba}: {resultado}")

def capturar_error(driver, nombre_prueba):
    path = f"screenshots/{nombre_prueba.replace(' ', '_')}.png"
    driver.save_screenshot(path)
    print(f"📸 Captura guardada: {path}")

def test_correo_invalido():
    nombre_prueba = "Crear usuario con correo inválido"
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("http://localhost/control/Control/login.php")
        driver.find_element(By.NAME, "user_name").send_keys("admin")
        driver.find_element(By.NAME, "user_password").send_keys("admin", Keys.RETURN)
        time.sleep(2)

        driver.get("http://localhost/control/Control/usuarios.php")
        nuevo_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Nuevo Usuario')]")))
        nuevo_btn.click()

        wait.until(EC.visibility_of_element_located((By.ID, "firstname"))).send_keys("Test")
        driver.find_element(By.ID, "lastname").send_keys("Correo")
        driver.find_element(By.ID, "user_name").send_keys("testcorreo")
        driver.find_element(By.ID, "user_email").send_keys("correo@invalido")  # <== inválido
        driver.find_element(By.ID, "user_password_new").send_keys("123456")
        driver.find_element(By.ID, "user_password_repeat").send_keys("123456")
        driver.find_element(By.XPATH, "//button[contains(text(), 'Guardar datos')]").click()

        time.sleep(2)

        # Buscar el mensaje de error (div con clase alert-danger)
        try:
            alerta = driver.find_element(By.CLASS_NAME, "alert-danger")
            if "correo electrónico no está en un formato" in alerta.text:
                guardar_resultado(nombre_prueba, "✅ Correo inválido fue rechazado correctamente")
            else:
                guardar_resultado(nombre_prueba, "❌ No se encontró el mensaje esperado")
                capturar_error(driver, nombre_prueba)
        except:
            guardar_resultado(nombre_prueba, "❌ No se detectó rechazo aunque el correo era inválido")
            capturar_error(driver, nombre_prueba)

    except Exception as e:
        guardar_resultado(nombre_prueba, f"❌ Error: {e}")
        capturar_error(driver, nombre_prueba)
    finally:
        driver.quit()

test_correo_invalido()

