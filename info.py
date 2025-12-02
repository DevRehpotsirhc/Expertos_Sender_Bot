import tkinter as tk

def show_info(root):
    win = tk.Toplevel(root)
    win.title("Programar tareas")
    win.geometry("420x350")
    win.resizable(False, False)

    # Centrar ventana
    win.update_idletasks()
    x = (win.winfo_screenwidth() - win.winfo_width()) // 2
    y = (win.winfo_screenheight() - win.winfo_height()) // 3
    win.geometry(f"+{x}+{y}")

    frame = tk.Frame(win, padx=20, pady=20)
    frame.pack(fill="both", expand=True)

    tk.Label(
        frame,
        text="Información",
        font=("Arial", 16, "bold"),
    ).pack(pady=(0, 10))

    texto = (
        "Esta aplicación permite:\n\n"
        "- Agregar múltiples tareas\n"
        "- Seleccionar un archivo para ejecutar en la terminal\n"
        "- Elegir hora exacta de ejecución\n"
        "- Definir correos de envío\n\n"
        "Las tareas incompletas no se guardarán."
    )

    tk.Label(
        frame,
        text=texto,
        justify="left",
        font=("Arial", 12),
    ).pack(pady=10)

    tk.Button(
        frame,
        text="Cerrar",
        command=win.destroy,
        width=12
    ).pack(pady=10)

    tk.Label(
        frame,
        text="Versión 1.0.0  •  Desarrollado por Christopher Aponte",
        font=("Arial", 9),
        fg="gray",
    ).pack(pady=(10, 0))