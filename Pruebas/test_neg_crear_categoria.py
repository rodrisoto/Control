from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import os

# Crear carpeta de capturas si no existe
os.makedirs("screenshots", exist_ok=True)

# Guardar resultado en un log
def guardar_resultado(nombre, mensaje):
    with open("resultados_categorias.txt", "a") as f:
        f.write(f"[{datetime.now()}] {nombre}: {mensaje}\n")
    print(f"{nombre}: {mensaje}")

# Test: intentar crear categoría sin completar campos
def test_crear_categoria_vacia():
    nombre_prueba = "Crear categoría vacía"
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

        # 3. Click en "Nueva Categoría"
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'Nueva Categoría')]"))
        ).click()

        # 4. Dejar campos vacíos y hacer clic en guardar
        wait.until(EC.visibility_of_element_located((By.NAME, "nombre"))).clear()
        driver.find_element(By.NAME, "descripcion").clear()
        driver.find_element(By.XPATH, "//button[contains(text(), 'Guardar datos')]").click()
        time.sleep(2)

        # 5. Verificar si no se creó categoría (asumiendo que la página no redirige)
        url_actual = driver.current_url
        if "categorias.php" in url_actual:
            guardar_resultado(nombre_prueba, "✅ No se permitió crear categoría vacía (correcto)")
        else:
            guardar_resultado(nombre_prueba, "❌ La categoría vacía fue aceptada (error)")
            driver.save_screenshot(f"screenshots/{nombre_prueba.replace(' ', '_')}.png")

    except Exception as e:
        driver.save_screenshot(f"screenshots/{nombre_prueba.replace(' ', '_')}.png")
        guardar_resultado(nombre_prueba, f"❌ Error inesperado: {e}")
    finally:
        driver.quit()

# Ejecutar
test_crear_categoria_vacia()

