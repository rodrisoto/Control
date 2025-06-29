from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from datetime import datetime

archivo_resultado = "resultados_login.txt"
os.makedirs("screenshots", exist_ok=True)

def guardar_resultado(nombre_prueba, resultado):
    with open(archivo_resultado, "a") as f:
        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{ahora}] {nombre_prueba}: {resultado}\n")
    print(f"{nombre_prueba}: {resultado}")

def capturar_error(driver, nombre_prueba):
    path = f"screenshots/{nombre_prueba.replace(' ', '_')}.png"
    driver.save_screenshot(path)
    print(f"📸 Captura guardada: {path}")

def test_editar_usuario_completo():
    nombre_prueba = "Editar usuario completo"
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        # Login
        driver.get("http://localhost/control/Control/login.php")
        driver.find_element(By.NAME, "user_name").send_keys("admin")
        driver.find_element(By.NAME, "user_password").send_keys("admin", Keys.RETURN)
        time.sleep(2)

        # Ir a usuarios
        driver.get("http://localhost/control/Control/usuarios.php")
        time.sleep(2)

        # Clic en el botón de editar
        editar_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[title='Editar usuario'][data-target='#myModal2']")))
        editar_btn.click()

        # Esperar y modificar campos
        wait.until(EC.visibility_of_element_located((By.ID, "firstname2"))).clear()
        driver.find_element(By.ID, "firstname2").send_keys("Rodrigo")

        wait.until(EC.visibility_of_element_located((By.ID, "lastname2"))).clear()
        driver.find_element(By.ID, "lastname2").send_keys("Soto")

        wait.until(EC.visibility_of_element_located((By.ID, "user_name2"))).clear()
        driver.find_element(By.ID, "user_name2").send_keys("rsoto")

        wait.until(EC.visibility_of_element_located((By.ID, "user_email2"))).clear()
        driver.find_element(By.ID, "user_email2").send_keys("rsoto@correo.com")

        # Click en Actualizar
        driver.find_element(By.ID, "actualizar_datos").click()
        time.sleep(2)

        # Verificar si los datos aparecen en la tabla
        page = driver.page_source
        if all(x in page for x in ["Rodrigo", "Soto", "rsoto", "rsoto@correo.com"]):
            guardar_resultado(nombre_prueba, "✅ Usuario actualizado correctamente")
        else:
            guardar_resultado(nombre_prueba, "❌ Los cambios no se reflejan correctamente")
            capturar_error(driver, nombre_prueba)

    except Exception as e:
        guardar_resultado(nombre_prueba, f"❌ Error: {e}")
        capturar_error(driver, nombre_prueba)

    driver.quit()

# Ejecutar
test_editar_usuario_completo()
