from utils import base_path
import tkinter as tk
from app import App
import subprocess
import os



def configurar_cron():
    script = base_path("setup_cron.sh")

    if os.path.isfile(script):
        subprocess.run(["bash", script], check=False)


configurar_cron()


root = tk.Tk()
root.geometry("650x600")
root.minsize(650, 600)
App(root)
root.mainloop()
