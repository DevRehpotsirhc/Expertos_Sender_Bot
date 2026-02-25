import os
import json
import smtplib
from pathlib import Path
from utils import base_path
from datetime import datetime
from dotenv import load_dotenv
from email.message import EmailMessage
from playwright.sync_api import sync_playwright, TimeoutError



load_dotenv(base_path(".env"))
DATA_FILE = base_path("data.json")

CORREO = os.environ.get("CORREO")
PASS_APP = os.environ.get("PASS_APP")

RUTA = Path.home() / "Documents"
with open(base_path("ipsdata.json"), "r") as f:
    IPS = json.load(f)

def crear_archivos():
    rutas_generadas = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for ip in IPS:
            print(f"Procesando {ip}...")

            carpeta_ip = f"{RUTA}/{ip}"
            os.makedirs(carpeta_ip, exist_ok=True)
            archivo = f"{carpeta_ip}/info_dispositivo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

            try:
                page = browser.new_page()
                page.goto(f"http://{ip}")

                page.wait_for_load_state("domcontentloaded")

                frame = page.frame_locator("frame[name='work']")

                menu = frame.locator("a.a_parent:has-text('Estado/Información')")
                menu.wait_for()
                menu.hover()

                item = frame.locator("ul.submenu a:has-text('Info dispositivo')")
                item.wait_for()
                item.click()

                page.wait_for_load_state("networkidle")
                frame.locator("tr.staticProp").first.wait_for()

                data = {}

                bloque_sistema = frame.locator("div.standard:has-text('Sistema')").locator(
                    "xpath=ancestor::table[1]/following::table[1]"
                )

                rows = bloque_sistema.locator("tr.staticProp").all()

                for row in rows:
                    tds = row.locator("td").all()
                    if len(tds) < 4:
                        continue

                    label = tds[1].inner_text().strip()

                    if len(tds) >= 5:
                        v1 = tds[3].inner_text().replace("\n", " ").strip()
                        v2 = tds[4].inner_text().replace("\n", " ").strip()
                        value = f"{v1} | {v2}"
                    else:
                        value = tds[3].inner_text().strip()

                    data[label] = value

                with open(archivo, "w", encoding="utf-8") as f:
                    for k, v in data.items():
                        f.write(f"{k}: {v}\n")
                
                page.goto(f"http://{ip}")
                page.wait_for_load_state("domcontentloaded")
                frame = page.frame_locator("frame[name='work']")
                
                menu = frame.locator("a.a_parent:has-text('Estado/Información')")
                menu.wait_for()
                menu.hover()

                item_contador = frame.locator("ul.submenu a:has-text('Contador')")
                item_contador.wait_for()
                item_contador.click()

                page.wait_for_load_state("networkidle")
                frame.locator("tr.staticProp").first.wait_for()

                data_contador = {}
                seccion_actual = "General"
                subseccion_actual = None

                rows = frame.locator("xpath=//tr[contains(@class,'staticProp')] | //div[@class='standard']").all()

                for row in rows:
                    tag = row.evaluate("el => el.tagName.toLowerCase()")

                    if tag == "div":
                        texto = row.inner_text().strip()
                        if texto:
                            seccion_actual = texto
                            subseccion_actual = None
                        continue

                    tds = row.locator("td").all()
                    textos = [td.inner_text().strip() for td in tds if td.inner_text().strip()]

                    if not textos:
                        continue

                    if len(textos) == 1:
                        subseccion_actual = textos[0]
                        continue

                    if len(textos) >= 3:
                        label = textos[0]
                        valor = textos[2]

                        if subseccion_actual:
                            key = f"{seccion_actual} - {subseccion_actual} - {label}"
                        else:
                            key = f"{seccion_actual} - {label}"

                        data_contador[key] = valor


                with open(archivo, "a", encoding="utf-8") as f:
                    f.write("\n=== CONTADOR ===\n")
                    for k, v in data_contador.items():
                        if str(v).strip().lower() == "atrás":
                            continue
                        if "atrás" in str(k).lower():
                            continue

                        f.write(f"{k}: {v}\n")  
                
            except (TimeoutError, Exception):
                with open(archivo, "w", encoding="utf-8") as f:
                    f.write("Hubo un problema al cargar la página\n")

                print(f"Ocurrió un problema con la ip: {ip}")

                try:
                    page.close()
                except:
                    pass

            finally:
                rutas_generadas.append(archivo)

        browser.close()
        
    return rutas_generadas


def enviar_correo(destinatarios, archivos_generados):
    if not archivos_generados:
        return

    msg = EmailMessage()
    msg["From"] = CORREO
    msg["To"] = ", ".join(destinatarios)
    msg["Subject"] = "Reporte de impresoras"

    cuerpo = []
    separador = "\n" + ("=" * 70) + "\n"

    for archivo in archivos_generados:
        if not os.path.exists(archivo):
            print(f"Archivo no existe: {archivo}")
            continue

        ip = os.path.basename(os.path.dirname(archivo))

        try:
            with open(archivo, "r", encoding="utf-8") as f:
                lineas = f.readlines()

            cuerpo.append(separador)
            cuerpo.append(f"ARCHIVO: {os.path.basename(archivo)}")
            cuerpo.append(f"IP: {ip}")
            cuerpo.append("-" * 70)
            cuerpo.append("")

            for linea in lineas:
                cuerpo.append(linea.rstrip("\n"))

            cuerpo.append("\n\n")

        except Exception as e:
            cuerpo.append(separador)
            cuerpo.append(f"ARCHIVO: {os.path.basename(archivo)}")
            cuerpo.append(f"IP: {ip}")
            cuerpo.append("(No se pudo leer el archivo)\n\n")
            print(f"Error leyendo {archivo}: {e}")

    cuerpo.append(separador)
    msg.set_content("\n".join(cuerpo))

    for archivo in archivos_generados:
        if not os.path.exists(archivo):
            continue
        try:
            with open(archivo, "rb") as f:
                msg.add_attachment(
                    f.read(),
                    maintype="application",
                    subtype="octet-stream",
                    filename=os.path.basename(archivo),
                )
        except Exception as e:
            print(f"No se pudo adjuntar {archivo}: {e}")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(CORREO, PASS_APP)
            smtp.send_message(msg)
            print("Correo enviado correctamente")
    except Exception as e:
        print(f"Error enviando correo: {e}")


def execute_scraper():
    hora = datetime.now().strftime("%H:%M")

    with open(DATA_FILE, "r") as f:
        tareas = json.load(f)

    for t in tareas:
        if hora in t["hora_imp"]:
            archivos_generados = crear_archivos()

            if archivos_generados:
                enviar_correo(t["correos"], archivos_generados)
                print(f"Archivos enviados a {t['correos']}")


if __name__ == '__main__':
    with open(DATA_FILE, "r") as f:
        tareas = json.load(f)

    for t in tareas:
        archivos_generados = crear_archivos()

        if archivos_generados:
            enviar_correo(t["correos"], archivos_generados)
            print(f"Archivos enviados a {t['correos']}")
