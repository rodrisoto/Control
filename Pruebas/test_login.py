
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

        if should_pass and "stock.php" in driver.current_url:
            guardar_resultado(nombre_prueba, f"✅ Éxito esperado (⏱ {duracion}s)")
        else:
            guardar_resultado(nombre_prueba, "❌ Resultado inesperado")
            capturar_error(driver, nombre_prueba)

    except Exception as e:
        guardar_resultado(nombre_prueba, f"❌ Error: {e}")
        capturar_error(driver, nombre_prueba)

    driver.quit()

def test_logout():
    nombre_prueba = "Logout después de login"
    driver = webdriver.Chrome()
    try:
        driver.get("http://localhost/Control/Control/login.php")
        time.sleep(1)

        driver.find_element(By.NAME, "user_name").send_keys("admin")
        driver.find_element(By.NAME, "user_password").send_keys("admin", Keys.RETURN)
        time.sleep(2)

        if "stock.php" in driver.current_url:
            try:
                logout = driver.find_element(By.LINK_TEXT, "Salir")
                logout.click()
                time.sleep(2)
                if "login.php" in driver.current_url:
                    guardar_resultado(nombre_prueba, "✅ Logout exitoso")
                else:
                    guardar_resultado(nombre_prueba, "❌ Logout no redirige correctamente")
                    capturar_error(driver, nombre_prueba)
            except:
                guardar_resultado(nombre_prueba, "❌ No se encontró botón/enlace de logout")
                capturar_error(driver, nombre_prueba)
        else:
            guardar_resultado(nombre_prueba, "❌ No se pudo hacer login previo")
            capturar_error(driver, nombre_prueba)

    except Exception as e:
        guardar_resultado(nombre_prueba, f"❌ Error: {e}")
        capturar_error(driver, nombre_prueba)
    driver.quit()

with open(archivo_resultado, "w") as f:
    f.write("RESULTADOS PRUEBAS LOGIN\n\n")

test_login("Login válido", "admin", "admin", True)
test_logout()
