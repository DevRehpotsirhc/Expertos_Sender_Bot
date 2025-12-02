import os
import json
from dotenv import load_dotenv
import subprocess
import smtplib
from email.message import EmailMessage
from datetime import datetime



BASE_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv(os.path.join(BASE_DIR, ".env"))
DATA_FILE = os.path.join(BASE_DIR, "data.json")
CORREO = os.environ.get("CORREO")
PASS_APP = os.environ.get("PASS_APP")



def ejecutar_script(ruta):
    res = subprocess.run(["bash", ruta], capture_output=True, text=True)
    return res.stdout.strip()

def enviar_correo(destinatarios, archivo):
    msg = EmailMessage()
    msg["From"] = CORREO
    msg["To"] = ", ".join(destinatarios)
    msg["Subject"] = "Archivo generado"

    with open(archivo, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="octet-stream",
            filename=archivo.split("/")[-1]
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(CORREO, PASS_APP)
        smtp.send_message(msg)

def main():
    hora = datetime.now().strftime("%H:%M")

    with open(DATA_FILE, "r") as f:
        tareas = json.load(f)

    for t in tareas:
        if t["hora"] == hora:
            salida = ejecutar_script(t["archivo"])
            enviar_correo(t["correos"], salida)

if __name__ == "__main__":
    main()
    
