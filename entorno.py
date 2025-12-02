import tkinter as tk
from tkinter import messagebox
import os

ENV_FILE = ".env"

class EnvVariableItem:
    def __init__(self, master, data=None, on_delete=None):
        self.frame = tk.Frame(master, bd=1, relief="solid", padx=5, pady=5)
        self.on_delete = on_delete

        # Nombre
        tk.Label(self.frame, text="Nombre:").grid(row=0, column=0, sticky="w")
        self.entry_name = tk.Entry(self.frame, width=20)
        self.entry_name.grid(row=0, column=1, padx=5)

        # Valor
        tk.Label(self.frame, text="Valor:").grid(row=0, column=2, sticky="w")
        self.entry_value = tk.Entry(self.frame, width=30)
        self.entry_value.grid(row=0, column=3, padx=5)

        # Botón eliminar
        tk.Button(self.frame, text="X", fg="red", command=self.delete).grid(row=0, column=4, padx=5)

        # Si vienen datos, los cargamos
        if data:
            self.entry_name.insert(0, data["name"])
            self.entry_value.insert(0, data["value"])

    def get_data(self):
        return {
            "name": self.entry_name.get().strip().upper(),
            "value": self.entry_value.get().strip()
        }

    def delete(self):
        if messagebox.askyesno("Eliminar", "¿Deseas eliminar esta variable?"):
            if self.on_delete:
                self.on_delete(self)
            self.frame.destroy()


class EnvWindow:
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel(root)
        self.window.title("Variables del .env")

        self.items_frame = tk.Frame(self.window)
        self.items_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.items = []

        # Cargar variables existentes
        self.load_existing()

        # Botón agregar variable
        tk.Button(self.window, text="Agregar +", command=self.add_item).pack(pady=5)

        # Botón guardar todas
        tk.Button(self.window, text="Guardar", command=self.save_all).pack(pady=5)

    def load_existing(self):
        if not os.path.exists(ENV_FILE):
            return
        with open(ENV_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if not line or "=" not in line:
                    continue
                name, value = line.split("=", 1)
                self.add_item({"name": name, "value": value})

    def add_item(self, data=None):
        item = EnvVariableItem(self.items_frame, data=data, on_delete=self.remove_item)
        item.frame.pack(pady=3, fill="x")
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def save_all(self):
        with open(ENV_FILE, "w") as f:
            for item in self.items:
                data = item.get_data()
                if data["name"] and data["value"]:
                    f.write(f"{data['name']}={data['value']}\n")
        messagebox.showinfo("Guardado", "Variables guardadas exitosamente")
