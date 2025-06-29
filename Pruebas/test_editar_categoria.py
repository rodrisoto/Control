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

def test_editar_categoria():
    nombre_prueba = "Editar categoría"
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

        # 3. Click en botón de editar
        boton_editar = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[@title='Editar categoría']")))
        boton_editar.click()

        # 4. Esperar el modal y completar campos
        input_nombre = wait.until(EC.visibility_of_element_located((By.ID, "mod_nombre")))
        input_descripcion = driver.find_element(By.ID, "mod_descripcion")

        input_nombre.clear()
        input_nombre.send_keys("Categoría actualizada")

        input_descripcion.clear()
        input_descripcion.send_keys("Descripción modificada por Selenium")

        # 5. Hacer clic en Actualizar
        boton_actualizar = driver.find_element(By.ID, "actualizar_datos")
        boton_actualizar.click()
        time.sleep(2)

        guardar_resultado(nombre_prueba, "✅ Categoría editada correctamente")

    except Exception as e:
        driver.save_screenshot(f"screenshots/{nombre_prueba.replace(' ', '_')}.png")
        guardar_resultado(nombre_prueba, f"❌ Error al editar categoría: {e}")
    finally:
        driver.quit()

test_editar_categoria()
