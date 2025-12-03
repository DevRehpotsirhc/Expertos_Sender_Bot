import tkinter as tk

def show_reque(root):
    win = tk.Toplevel(root)
    win.title("Programar tareas")
    win.geometry("420x400")
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
        text="Requerimientos",
        font=("Arial", 16, "bold"),
    ).pack(pady=(0, 10))

    texto = (
        "Para el correcto funcionamiento del\n"
        "sistema, siga estos pasos:\n\n"
        " - Añada la clave de aplicación (correo) al entorno\n"
        " - Añada el correo vinculado a la clave al entorno\n"
        " - Asigne las tareas con 1 min de diferencia al menos\n"
        " - Asegurate de tener crontab enrutado al sistema\n\n"
        "Las variables de entorno para el correo y clave deben\n"
        "llamarse CORREO y PASS_APP respectivamente"
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
