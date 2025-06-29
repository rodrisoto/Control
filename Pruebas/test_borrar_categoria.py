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
    with open("resultados_categorias.txt", "a") as f:
        f.write(f"[{datetime.now()}] {nombre}: {mensaje}\n")
    print(f"{nombre}: {mensaje}")

def test_borrar_categoria():
    nombre_prueba = "Borrar categoría"
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        # 1. Login
        driver.get("http://localhost/control/Control/login.php")
        driver.find_element(By.NAME, "user_name").send_keys("admin")
        driver.find_element(By.NAME, "user_password").send_keys("admin", Keys.RETURN)
        time.sleep(2)

        # 2. Ir a Categorías
        driver.get("http://localhost/control/Control/categorias.php")
        time.sleep(2)

        # 3. Buscar botón de borrar (ícono de papelera con onclick eliminar(ID))
        boton_borrar = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(@onclick,'eliminar(')]")))
        boton_borrar.click()

        # 4. Esperar un momento por la eliminación (si no hay confirmación)
        time.sleep(2)

        guardar_resultado(nombre_prueba, "✅ Categoría borrada correctamente")

    except Exception as e:
        driver.save_screenshot(f"screenshots/{nombre_prueba.replace(' ', '_')}.png")
        guardar_resultado(nombre_prueba, f"❌ Error al borrar categoría: {e}")
    finally:
        driver.quit()

test_borrar_categoria()
