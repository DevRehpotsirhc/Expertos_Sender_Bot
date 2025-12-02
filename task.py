import tkinter as tk
from tkinter import filedialog, messagebox
import tkinter.ttk as ttk

class TaskItem:
    def __init__(self, master, data=None, on_delete=None):
        self.frame = tk.Frame(master, bd=2, relief="groove", padx=5, pady=5)

        self.on_delete = on_delete

        # ----- Archivo -----
        tk.Label(self.frame, text="Archivo:").grid(row=0, column=0, sticky="w")
        self.entry_archivo = tk.Entry(self.frame, width=40)
        self.entry_archivo.grid(row=0, column=1)
        tk.Button(self.frame, text="Seleccionar", command=self.seleccionar_archivo)\
            .grid(row=0, column=2)

        # ----- Hora -----
        tk.Label(self.frame, text="Hora:").grid(row=1, column=0, sticky="w")

        horas = [f"{h:02d}" for h in range(24)]
        minutos = [f"{m:02d}" for m in range(60)]

        self.combo_hora = ttk.Combobox(self.frame, values=horas, width=5, state="readonly")
        self.combo_hora.grid(row=1, column=1, sticky="w")

        self.combo_minuto = ttk.Combobox(self.frame, values=minutos, width=5, state="readonly")
        self.combo_minuto.grid(row=1, column=1, padx=60, sticky="w")

        # ----- Correos -----
        tk.Label(self.frame, text="Correos destino:").grid(row=2, column=0, sticky="w")
        self.entry_correos = tk.Entry(self.frame, width=30)
        self.entry_correos.grid(row=2, column=1)

        # ----- Botón eliminar -----
        tk.Button(self.frame, text="X", fg="red", command=self.delete)\
            .grid(row=0, column=3, rowspan=3, padx=10)

        # Cargar datos si vienen de archivo
        if data:
            self.entry_archivo.insert(0, data["archivo"])
            h, m = data["hora"].split(":")
            self.combo_hora.set(h)
            self.combo_minuto.set(m)

            # Correos: si viene lista → convertir a string con comas
            if isinstance(data["correos"], list):
                self.entry_correos.insert(0, ", ".join(data["correos"]))
            else:
                self.entry_correos.insert(0, data["correos"])
        else:
            self.combo_hora.set("00")
            self.combo_minuto.set("00")

    def seleccionar_archivo(self):
        ruta = filedialog.askopenfilename()
        if ruta:
            self.entry_archivo.delete(0, tk.END)
            self.entry_archivo.insert(0, ruta)

    def get_data(self):
        correos = [c.strip() for c in self.entry_correos.get().split(",") if c.strip()]

        return {
            "archivo": self.entry_archivo.get(),
            "hora": f"{self.combo_hora.get()}:{self.combo_minuto.get()}",
            "correos": correos
        }

    def delete(self):
        confirmar = messagebox.askyesno(
            "Eliminar",
            "¿Deseas eliminar esta tarea?"
        )
        if not confirmar:
            return

        if self.on_delete:
            self.on_delete(self)

        self.frame.destroy()