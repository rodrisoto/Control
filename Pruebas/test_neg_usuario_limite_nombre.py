from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
import os

os.makedirs("screenshots", exist_ok=True)
archivo_resultado = "resultados_usuarios.txt"

def guardar_resultado(nombre, mensaje):
    with open(archivo_resultado, "a") as f:
        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{ahora}] {nombre}: {mensaje}\n")
    print(f"{nombre}: {mensaje}")

def test_usuario_limite_nombre():
    nombre_prueba = "Crear usuario con nombre muy largo"
    driver = webdriver.Chrome()
    try:
        driver.get("http://localhost/control/Control/login.php")
        driver.find_element(By.NAME, "user_name").send_keys("admin")
        driver.find_element(By.NAME, "user_password").send_keys("admin", Keys.RETURN)
        time.sleep(2)

        driver.get("http://localhost/control/Control/usuarios.php")
        time.sleep(1)
        driver.find_element(By.ID, "addUserBtn").click()
        time.sleep(1)

        nombre_largo = "X" * 300
        driver.find_element(By.ID, "nombre").send_keys(nombre_largo)
        driver.find_element(By.ID, "apellido").send_keys("Limite")
        driver.find_element(By.ID, "usuario").send_keys("limitex")
        driver.find_element(By.ID, "email").send_keys("limitex@correo.com")
        driver.find_element(By.ID, "clave").send_keys("123456")
        driver.find_element(By.ID, "guardar_datos").click()
        time.sleep(2)

        mensaje_error = driver.find_element(By.ID, "resultados_ajax").text
        if "longitud" in mensaje_error.lower() or "error" in mensaje_error.lower():
            guardar_resultado(nombre_prueba, "✅ Detectó nombre demasiado largo")
        else:
            guardar_resultado(nombre_prueba, "❌ No se detectó límite de caracteres")
            driver.save_screenshot(f"screenshots/{nombre_prueba.replace(' ', '_')}.png")
    except Exception as e:
        guardar_resultado(nombre_prueba, f"❌ Error: {e}")
    finally:
        driver.quit()

test_usuario_limite_nombre()
