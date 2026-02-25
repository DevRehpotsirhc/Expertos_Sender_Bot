from tkinter import filedialog, messagebox
import tkinter as tk



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
        tk.Label(self.frame, text="Hora(s):").grid(row=1, column=0, sticky="w")

        self.entry_horas = tk.Entry(self.frame, width=20)
        self.entry_horas.grid(row=1, column=1, sticky="w")

        # ----- Correos -----
        tk.Label(self.frame, text="Correos:").grid(row=2, column=0, sticky="w")
        self.entry_correos = tk.Entry(self.frame, width=30)
        self.entry_correos.grid(row=2, column=1)

        # ----- Botón eliminar -----
        tk.Button(self.frame, text="X", fg="red", command=self.delete)\
            .grid(row=0, column=3, rowspan=3, padx=10)

        if data:
            self.entry_archivo.insert(0, ", ".join(data["archivos"]) if isinstance(data["archivos"], list) else data["archivos"])

            # Horas (lista o string)
            if isinstance(data["horas"], list):
                self.entry_horas.insert(0, ", ".join(data["horas"]))
            else:
                self.entry_horas.insert(0, data["horas"])

            # Correos
            if isinstance(data["correos"], list):
                self.entry_correos.insert(0, ", ".join(data["correos"]))
            else:
                self.entry_correos.insert(0, data["correos"])


    def seleccionar_archivo(self):
        rutas = filedialog.askopenfilenames()
        if rutas:
            self.entry_archivo.delete(0, tk.END)
            self.entry_archivo.insert(0, ", ".join(rutas))


    def get_data(self):
        archivos = [a.strip() for a in self.entry_archivo.get().split(",") if a.strip()]
        horas = [h.strip() for h in self.entry_horas.get().split(",") if h.strip()]
        correos = [c.strip() for c in self.entry_correos.get().split(",") if c.strip()]

        return {
            "archivos": archivos,
            "horas": horas,
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