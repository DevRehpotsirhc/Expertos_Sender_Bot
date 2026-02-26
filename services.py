from email.message import EmailMessage
from dotenv import load_dotenv
from datetime import datetime
from utils import base_path
import subprocess
import smtplib
import json
import os



load_dotenv(base_path(".env"))
DATA_FILE = base_path("data.json")

CORREO = os.environ.get("CORREO")
PASS_APP = os.environ.get("PASS_APP")


def ejecutar_script(ruta):
    """_Función que lee un archivo .sh y lo ejecuta_

    Args:
        ruta: _dirección del archivo a ejecutar_

    Returns:
        _response_: _resultado del script_
    """
    res = subprocess.run(["bash", ruta], capture_output=True, text=True)
    return res.stdout.strip()


def enviar_correo(destinatarios, archivos_generados):
    """_Función encargada de desglosar los
    archivos generados en el cuerpo de un correo y
    enviarlo a los destinatarios asignados_

    Args:
        destinatarios (_list_): _lista de correos_
        archivos_generados (_list_): _lista de rutas_
    """
    msg = EmailMessage()
    msg["From"] = CORREO
    msg["To"] = ", ".join(destinatarios)
    msg["Subject"] = "Reporte de Servicios - Archivos generados"

    cuerpo = []

    for archivo in archivos_generados:
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                lineas = f.readlines()

            cuerpo.append(f"===== {os.path.basename(archivo)} =====")

            # Detectar encabezado y separadores
            for linea in lineas:
                raw = linea.rstrip("\n")

                # Saltar líneas vacías
                if not raw.strip():
                    cuerpo.append("")
                    continue

                # Mantener la línea de separación tal cual
                if set(raw) == {"-"} or {"|"}:
                    cuerpo.append(raw)
                    continue

                # Separar columnas por |
                if "|" in raw:
                    cols = [c.strip() for c in raw.split("|")]
                else:
                    cols = raw.split()

                # Tabular columnas
                if len(cols) >= 3:
                    col1 = cols[0].ljust(20)
                    col2 = cols[1].ljust(30)
                    col3 = cols[2].ljust(10)
                    cuerpo.append(f"{col1}{col2}{col3}")
                else:
                    cuerpo.append(raw)

            cuerpo.append("")

        except:
            cuerpo.append(f"===== {os.path.basename(archivo)} =====")
            cuerpo.append("(No es archivo de texto)\n")

    html = "<pre style='font-family: monospace; font-size: 13px;'>" + \
       "\n".join(cuerpo) + "</pre>"

    msg.add_alternative(html, subtype="html")

    for archivo in archivos_generados:
        with open(archivo, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="octet-stream",
                filename=os.path.basename(archivo)
            )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(CORREO, PASS_APP)
        smtp.send_message(msg)


def execute_services():
    """_Función que se encarga de ejecutar tanto el
    script como el envío de correos si se cumple el
    horario definido_
    """
    hora = datetime.now().strftime("%H:%M")

    with open(DATA_FILE, "r") as f:
        tareas = json.load(f)

    for t in tareas:
        if hora in t["horas"]:
            archivos_generados = []

            for archivo in t["archivos"]:
                salida = ejecutar_script(archivo)

                if os.path.exists(salida):
                    archivos_generados.append(salida)
                else:
                    print(f"El script {archivo} devolvió una ruta inválida: {salida}")

            if archivos_generados:
                enviar_correo(t["correos"], archivos_generados)
                print(f"Archivos envíados a {t['correos']}")
