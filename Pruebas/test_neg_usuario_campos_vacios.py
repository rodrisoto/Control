from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import os

os.makedirs("screenshots", exist_ok=True)
archivo_resultado = "resultados_usuarios.txt"

def guardar_resultado(nombre, mensaje):
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(archivo_resultado, "a") as f:
        f.write(f"[{ahora}] {nombre}: {mensaje}\n")
    print(f"{nombre}: {mensaje}")

def test_usuario_campos_vacios():
    nombre_prueba = "Crear usuario con campos vacíos"
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("http://localhost/control/Control/login.php")
        driver.find_element(By.NAME, "user_name").send_keys("admin")
        driver.find_element(By.NAME, "user_password").send_keys("admin", Keys.RETURN)
        time.sleep(2)

        driver.get("http://localhost/control/Control/usuarios.php")

        # Espera y clic en botón "Nuevo Usuario"
        nuevo_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Nuevo Usuario')]")))
        nuevo_btn.click()

        # Esperar el modal activo
        wait.until(EC.visibility_of_element_located((By.ID, "myModal")))
        time.sleep(1)

        # Intentar guardar con campos vacíos
        guardar_btn = driver.find_element(By.ID, "guardar_datos")
        guardar_btn.click()
        time.sleep(1)

        # Detectar si aún sigue el modal abierto (no cerró = no guardó)
        modal_visible = driver.find_element(By.ID, "myModal").is_displayed()

        if modal_visible:
            guardar_resultado(nombre_prueba, "✅ No se permitió guardar con campos vacíos")
        else:
            guardar_resultado(nombre_prueba, "❌ Se permitió guardar con campos vacíos")
            driver.save_screenshot("screenshots/usuario_campos_vacios.png")

    except Exception as e:
        guardar_resultado(nombre_prueba, f"❌ Error: {e}")
    finally:
        driver.quit()

test_usuario_campos_vacios()


