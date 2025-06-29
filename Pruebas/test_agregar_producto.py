from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
import os
from datetime import datetime

# Config
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

def test_agregar_producto():
    nombre_prueba = "Agregar producto"
    driver = webdriver.Chrome()
    try:
        # Login
        driver.get("http://localhost/control/Control/login.php")
        driver.find_element(By.NAME, "user_name").send_keys("admin")
        driver.find_element(By.NAME, "user_password").send_keys("admin", Keys.RETURN)
        time.sleep(2)

        # Ir a stock.php
        driver.get("http://localhost/control/Control/stock.php")
        time.sleep(1)

        # Click en el botón "+ Agregar"
        agregar_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Agregar')]")
        agregar_btn.click()
        time.sleep(1)

        # Rellenar formulario del modal
        driver.find_element(By.ID, "codigo").send_keys("P1001")
        driver.find_element(By.ID, "nombre").send_keys("Producto de prueba")
        Select(driver.find_element(By.ID, "categoria")).select_by_index(1)  # o select_by_value("1")
        driver.find_element(By.ID, "precio").send_keys("9990")
        driver.find_element(By.ID, "stock").send_keys("5")

        # Guardar
        driver.find_element(By.ID, "guardar_datos").click()
        time.sleep(2)

        # Verificar si aparece mensaje de éxito
        if "Producto de prueba" in driver.page_source:
            guardar_resultado(nombre_prueba, "✅ Producto agregado exitosamente")
        else:
            guardar_resultado(nombre_prueba, "❌ Producto no aparece")
            capturar_error(driver, nombre_prueba)

    except Exception as e:
        guardar_resultado(nombre_prueba, f"❌ Error: {e}")
        capturar_error(driver, nombre_prueba)

    driver.quit()

# Ejecutar prueba
test_agregar_producto()
