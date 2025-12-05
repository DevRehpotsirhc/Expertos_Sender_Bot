from task import TaskItem
import tkinter as tk
from requerimientos import show_reque
from info import show_info
from entorno import EnvWindow
from tkinter import messagebox
import json
import os
from utils import resource_path, base_path


CONFIG_FILE = base_path("data.json")
print(CONFIG_FILE)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Programar tareas")

        self.tasks = []

        header = tk.Frame(root, pady=10)
        header.pack(fill="x")

        tk.Button(header, text="info", command=lambda: show_info(self.root))\
            .pack(side="right", padx=10)
        
        tk.Button(header, text="requerimientos", command=lambda: show_reque(self.root))\
            .pack(side="right", padx=10)
        
        tk.Button(header, text="entorno", command=lambda: EnvWindow(self.root))\
            .pack(side="right", padx=10)

        # Contenedor de tareas
        container = tk.Frame(root)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        canvas = tk.Canvas(container)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Frame interno donde van las tareas
        self.frame_tasks = tk.Frame(canvas)
        canvas.create_window((0, 0), window=self.frame_tasks, anchor="nw")
        self.frame_tasks.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        def _on_mousewheel(event):
            if event.num == 4:      # scroll arriba
                canvas.yview_scroll(-1, "units")
            elif event.num == 5:    # scroll abajo
                canvas.yview_scroll(1, "units")

        canvas.bind_all("<Button-4>", _on_mousewheel)
        canvas.bind_all("<Button-5>", _on_mousewheel)

        # Botón agregar tarea
        tk.Button(root, text="Agregar +", command=self.add_task)\
            .pack(pady=10)

        # Botón guardar
        tk.Button(root, text="Guardar", command=self.save)\
            .pack(pady=10)

        self.load_tasks()

    def add_task(self, data=None):
        task = TaskItem(self.frame_tasks, data=data, on_delete=self.remove_task)
        task.frame.pack(pady=5, fill="x")
        self.tasks.append(task)

    def remove_task(self, task):
        self.tasks.remove(task)

    def save(self):
        data = []
        incompletas = 0

        for task in self.tasks:
            info = task.get_data()

            # Validar listas vacías
            if len(info["archivos"]) == 0 or len(info["correos"]) == 0 or len(info["horas"]) == 0:
                incompletas += 1
                continue

            data.append(info)

        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=4)

        if incompletas > 0:
            messagebox.showwarning(
                "Advertencia",
                "Algunas tareas no se guardaron porque les falta información (archivos/horas/correos)."
            )

        messagebox.showinfo(
            "Guardado",
            "Los datos se han guardado exitosamente"
        )

        print("Guardado:", data)


    def load_tasks(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                tareas = json.load(f)
            for t in tareas:
                self.add_task(t)
        else:
            self.add_task()