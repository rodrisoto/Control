from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import os
import time

os.makedirs("screenshots", exist_ok=True)

def guardar_resultado(nombre, mensaje):
    with open("resultados_login.txt", "a") as f:
        f.write(f"[{datetime.now()}] {nombre}: {mensaje}\n")
    print(f"{nombre}: {mensaje}")

def test_cambiar_contrasena():
    nombre_prueba = "Cambiar contraseña"
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        # 1. Login
        driver.get("http://localhost/control/Control/login.php")
        driver.find_element(By.NAME, "user_name").send_keys("admin")
        driver.find_element(By.NAME, "user_password").send_keys("admin", Keys.RETURN)
        time.sleep(2)

        # 2. Ir a usuarios
        driver.get("http://localhost/control/Control/usuarios.php")
        time.sleep(2)

        # 3. Click en botón "Cambiar contraseña" (ícono de llave)
        cambiar_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[@title='Cambiar contraseña']")))
        cambiar_btn.click()

        # 4. Esperar campos del modal y escribir nueva contraseña
        wait.until(EC.visibility_of_element_located((By.ID, "user_password_new3"))).send_keys("1234567")
        driver.find_element(By.ID, "user_password_repeat3").send_keys("1234567")

        # 5. Click en botón "Cambiar contraseña"
        boton_guardar = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'Cambiar contraseña')]")))
        boton_guardar.click()
        time.sleep(2)

        guardar_resultado(nombre_prueba, "✅ Contraseña cambiada exitosamente")

    except Exception as e:
        driver.save_screenshot(f"screenshots/{nombre_prueba.replace(' ', '_')}.png")
        guardar_resultado(nombre_prueba, f"❌ Error: {e}")
    finally:
        driver.quit()

test_cambiar_contrasena()
