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

def test_borrar_usuario():
    nombre_prueba = "Borrar usuario"
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("http://localhost/control/Control/login.php")
        driver.find_element(By.NAME, "user_name").send_keys("admin")
        driver.find_element(By.NAME, "user_password").send_keys("admin", Keys.RETURN)
        time.sleep(2)

        driver.get("http://localhost/control/Control/usuarios.php")
        time.sleep(2)

        eliminar_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[@title='Borrar usuario']")))
        eliminar_btn.click()

        WebDriverWait(driver, 5).until(EC.alert_is_present()).accept()
        time.sleep(2)

        guardar_resultado(nombre_prueba, "✅ Usuario borrado correctamente")

    except Exception as e:
        driver.save_screenshot(f"screenshots/{nombre_prueba.replace(' ', '_')}.png")
        guardar_resultado(nombre_prueba, f"❌ Error: {e}")
    finally:
        driver.quit()

test_borrar_usuario()
