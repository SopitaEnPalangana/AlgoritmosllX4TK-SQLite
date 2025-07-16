import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class LoginWindow(tk.Tk):
    """Pantalla de inicio de sesión."""
    def __init__(self):
        super().__init__()
        self.title("Login - Repair Center")
        self.geometry("300x200")
        self.resizable(False, False)

        ttk.Label(self, text="Usuario:").pack(pady=(20, 0))
        self.var_usuario = tk.StringVar()
        ttk.Entry(self, textvariable=self.var_usuario).pack(pady=5)

        ttk.Label(self, text="Contraseña:").pack(pady=(10, 0))
        self.var_clave = tk.StringVar()
        ttk.Entry(self, textvariable=self.var_clave, show="*").pack(pady=5)

        ttk.Button(self, text="Ingresar", command=self.verificar_login).pack(pady=20)

    def verificar_login(self):
        usuario = self.var_usuario.get()
        clave = self.var_clave.get()
        if usuario == "admin" and clave == "1234":
            self.destroy()
            app = RepairCenterApp()
            app.mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")


class RepairCenterApp(tk.Tk):
    """App para administrar pedidos de servicio técnico."""

    def __init__(self):
        super().__init__()
        self.title("Repair Center - Gestión de Pedidos")
        self.geometry("720x500")
        self.resizable(False, False)

        # -------- Datos en memoria (lista de diccionarios) -------- #
        self.pedidos = []

        # ---------------------------------------------------------- #
        # FORMULARIO
        # ---------------------------------------------------------- #
        frm_form = ttk.LabelFrame(self, text="Nuevo Pedido", padding=10)
        frm_form.pack(fill="x", padx=10, pady=10)

        # Apellido y Nombre
        ttk.Label(frm_form, text="Apellido y Nombre:").grid(row=0, column=0, sticky="w")
        self.var_nombre = tk.StringVar()
        ttk.Entry(frm_form, textvariable=self.var_nombre, width=40).grid(row=0, column=1, sticky="w")

        # Dirección
        ttk.Label(frm_form, text="Dirección (calle y altura):").grid(row=1, column=0, sticky="w", pady=(5, 0))
        self.var_direccion = tk.StringVar()
        ttk.Entry(frm_form, textvariable=self.var_direccion, width=40).grid(row=1, column=1, sticky="w", pady=(5, 0))

        # Inconveniente
        ttk.Label(frm_form, text="Inconveniente:").grid(row=2, column=0, sticky="w", pady=(5, 0))
        self.var_inconveniente = tk.StringVar()
        ttk.Entry(frm_form, textvariable=self.var_inconveniente, width=40).grid(row=2, column=1, sticky="w", pady=(5, 0))

        # Técnico asignado
        ttk.Label(frm_form, text="Técnico asignado:").grid(row=3, column=0, sticky="w", pady=(5, 0))
        self.var_tecnico = tk.StringVar()
        ttk.Combobox(frm_form, textvariable=self.var_tecnico, values=[
            "Juan Pérez", "María López", "Carlos Díaz", "Ana Gómez"
        ], width=37).grid(row=3, column=1, sticky="w", pady=(5, 0))

        # Fecha y hora
        ttk.Label(frm_form, text="Fecha y hora (AAAA-MM-DD HH:MM):").grid(row=4, column=0, sticky="w", pady=(5, 0))
        self.var_fecha = tk.StringVar()
        ttk.Entry(frm_form, textvariable=self.var_fecha, width=40).grid(row=4, column=1, sticky="w", pady=(5, 0))

        # Botón guardar
        ttk.Button(frm_form, text="Guardar Pedido", command=self.guardar_pedido).grid(row=5, column=0, columnspan=2, pady=10)

        # ---------------------------------------------------------- #
        # TABLA DE PEDIDOS
        # ---------------------------------------------------------- #
        columnas = ("cliente", "direccion", "inconveniente", "tecnico", "fecha")
        self.tree = ttk.Treeview(self, columns=columnas, show="headings", height=10)
        for col, titulo in zip(columnas, [
            "Cliente", "Dirección", "Inconveniente", "Técnico", "Fecha y hora"
        ]):
            self.tree.heading(col, text=titulo)
            self.tree.column(col, width=130, anchor="center")
        self.tree.pack(fill="both", padx=10, pady=(0, 10), expand=True)

    def guardar_pedido(self):
        nombre = self.var_nombre.get().strip()
        direccion = self.var_direccion.get().strip()
        inconveniente = self.var_inconveniente.get().strip()
        tecnico = self.var_tecnico.get().strip()
        fecha_txt = self.var_fecha.get().strip()

        if not all([nombre, direccion, inconveniente, tecnico, fecha_txt]):
            messagebox.showwarning("Datos incompletos", "Complete todos los campos.")
            return
        try:
            fecha = datetime.strptime(fecha_txt, "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Formato de fecha incorrecto", "Use AAAA-MM-DD HH:MM")
            return

        pedido = {
            "cliente": nombre,
            "direccion": direccion,
            "inconveniente": inconveniente,
            "tecnico": tecnico,
            "fecha": fecha.strftime("%Y-%m-%d %H:%M")
        }
        self.pedidos.append(pedido)
        self._agregar_a_tabla(pedido)
        self._limpiar_formulario()
        messagebox.showinfo("Guardado", "Pedido registrado con éxito.")

    def _agregar_a_tabla(self, pedido: dict):
        self.tree.insert("", tk.END, values=(
            pedido["cliente"], pedido["direccion"], pedido["inconveniente"], pedido["tecnico"], pedido["fecha"]
        ))

    def _limpiar_formulario(self):
        self.var_nombre.set("")
        self.var_direccion.set("")
        self.var_inconveniente.set("")
        self.var_tecnico.set("")
        self.var_fecha.set("")


if __name__ == "__main__":
    login = LoginWindow()
    login.mainloop()