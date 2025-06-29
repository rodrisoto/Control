
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
import os

archivo_resultado = "resultados_login.txt"
os.makedirs("screenshots", exist_ok=True)

def guardar_resultado(nombre_prueba, resultado):
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(archivo_resultado, "a") as f:
        f.write(f"[{ahora}] {nombre_prueba}: {resultado}\n")
    print(f"{nombre_prueba}: {resultado}")

def capturar_error(driver, nombre_prueba):
    nombre = f"screenshots/{nombre_prueba.replace(' ', '_')}.png"
    driver.save_screenshot(nombre)
    print(f"📸 Captura de error guardada: {nombre}")

def test_login(nombre_prueba, usuario, clave, should_pass):
    driver = webdriver.Chrome()
    driver.get("http://localhost/Control/Control/login.php")
    time.sleep(1)

    try:
        username_input = driver.find_element(By.NAME, "user_name")
        password_input = driver.find_element(By.NAME, "user_password")

        username_input.clear()
        password_input.clear()

        username_input.send_keys(usuario)
        password_input.send_keys(clave)

        start = time.time()
        password_input.send_keys(Keys.RETURN)
        time.sleep(2)
        end = time.time()
        duracion = round(end - start, 2)

        if not should_pass and "login.php" in driver.current_url:
            guardar_resultado(nombre_prueba, f"✅ Fallo esperado (⏱ {duracion}s)")
        else:
            guardar_resultado(nombre_prueba, "❌ Resultado inesperado")
            capturar_error(driver, nombre_prueba)

    except Exception as e:
        guardar_resultado(nombre_prueba, f"❌ Error: {e}")
        capturar_error(driver, nombre_prueba)

    driver.quit()

test_login("Contraseña incorrecta", "admin", "malaclave", False)
test_login("Usuario inexistente", "falso", "admin", False)
test_login("Campos vacíos", "", "", False)
test_login("Intento SQL Injection", "admin' --", "123", False)
