from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from datetime import datetime

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

def test_neg_editar_usuario_vacio():
    nombre_prueba = "Editar usuario con campos vacíos"
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("http://localhost/control/Control/login.php")
        driver.find_element(By.NAME, "user_name").send_keys("admin")
        driver.find_element(By.NAME, "user_password").send_keys("admin", Keys.RETURN)
        time.sleep(2)

        driver.get("http://localhost/control/Control/usuarios.php")
        time.sleep(2)

        editar_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[title='Editar usuario'][data-target='#myModal2']")))
        editar_btn.click()
        time.sleep(1)

        # Borrar campos requeridos
        campos = ["firstname2", "lastname2", "user_name2", "user_email2"]
        for campo in campos:
            campo_input = wait.until(EC.visibility_of_element_located((By.ID, campo)))
            campo_input.clear()

        # Click en guardar
        driver.find_element(By.ID, "actualizar_datos").click()
        time.sleep(2)

        # Verificar si hay errores en los campos o no se cerró el modal
        modal_visible = driver.find_element(By.ID, "myModal2").is_displayed()
        if modal_visible:
            guardar_resultado(nombre_prueba, "✅ Edición rechazada por campos vacíos")
        else:
            guardar_resultado(nombre_prueba, "❌ Se permitió edición con campos vacíos")
            capturar_error(driver, nombre_prueba)

    except Exception as e:
        guardar_resultado(nombre_prueba, f"❌ Error inesperado: {e}")
        capturar_error(driver, nombre_prueba)

    driver.quit()

# Ejecutar
test_neg_editar_usuario_vacio()

