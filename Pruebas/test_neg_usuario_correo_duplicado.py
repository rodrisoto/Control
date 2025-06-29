from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import os

archivo_resultado = "resultados_usuarios.txt"
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

def test_usuario_correo_duplicado():
    nombre_prueba = "Crear usuario con correo duplicado"
    correo_duplicado = "japerez@correo.com"  # Asegúrate de que este correo ya exista en la BD

    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        # Login
        driver.get("http://localhost/control/Control/login.php")
        driver.find_element(By.NAME, "user_name").send_keys("admin")
        driver.find_element(By.NAME, "user_password").send_keys("admin", Keys.RETURN)
        time.sleep(2)

        # Ir a Usuarios
        driver.get("http://localhost/control/Control/usuarios.php")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Nuevo Usuario')]"))).click()
        time.sleep(1)

        # Llenar datos con correo duplicado
        wait.until(EC.visibility_of_element_located((By.ID, "firstname"))).send_keys("Duplicado")
        driver.find_element(By.ID, "lastname").send_keys("Soto")
        driver.find_element(By.ID, "user_name").send_keys("Cucho")
        driver.find_element(By.ID, "user_email").send_keys(correo_duplicado)
        driver.find_element(By.ID, "user_password_new").send_keys("123456")
        driver.find_element(By.ID, "user_password_repeat").send_keys("123456")

        # Guardar
        driver.find_element(By.XPATH, "//button[contains(text(), 'Guardar datos')]").click()
        time.sleep(2)

        # Buscar mensaje de error
        alertas = driver.find_elements(By.CLASS_NAME, "alert-danger")
        if any("ya está en uso" in a.text.lower() or "correo electrónico" in a.text.lower() for a in alertas):
            guardar_resultado(nombre_prueba, "✅ Rechazo por correo duplicado correcto")
        else:
            guardar_resultado(nombre_prueba, "❌ Se permitió un correo duplicado")
            capturar_error(driver, nombre_prueba)

    except Exception as e:
        guardar_resultado(nombre_prueba, f"❌ Error: {e}")
        capturar_error(driver, nombre_prueba)

    finally:
        driver.quit()

test_usuario_correo_duplicado()



