import os
import json
from dotenv import load_dotenv
import subprocess
import smtplib
from email.message import EmailMessage
from datetime import datetime
import os
from utils import resource_path, base_path



load_dotenv(base_path(".env"))
DATA_FILE = base_path("data.json")

CORREO = os.environ.get("CORREO")
PASS_APP = os.environ.get("PASS_APP")


def ejecutar_script(ruta):
    res = subprocess.run(["bash", ruta], capture_output=True, text=True)
    return res.stdout.strip()

def enviar_correo(destinatarios, archivos_generados):
    msg = EmailMessage()
    msg["From"] = CORREO
    msg["To"] = ", ".join(destinatarios)
    msg["Subject"] = "Reporte de Servicios - Archivos generados"

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


def main():
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


if __name__ == "__main__":
    main()
    
