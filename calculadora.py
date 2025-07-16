#3.1 Construir una calculadora (suma, resta, multiplicar y dividir)
import tkinter as tk
from tkinter import ttk


class Calculadora(tk.Tk):   #la calculadora hereda de la ventana principal

    def __init__(self):
        super().__init__()
        self.title("Calculadora")
        self.geometry("260x350")
        self.resizable(False, False)

        # ---------- Estado interno ---------- #
        self.expresion: str = ""  # vriable para guardar lo que se va escribiendo

        # ---------- Pantalla/Display ---------- #
        self.display = ttk.Entry(self, font=("Helvetica", 20), justify="right")  #el campo de texto donde se muestra la expresion
        self.display.pack(fill="x", padx=10, pady=(15, 5))   #posiciona el widget dentro de la ventana, en este caso ocupa casi todo
        self.display.configure(state="readonly")    #hace que no se pueda escribir directamente, tiene que ingresar con los botones

        # ---------- Botones ---------- #
        botones = [
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("÷", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("×", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
            ("C", 5, 0),
        ]

        marco = ttk.Frame(self)   # el frame esta dentro de la calculadora. es una caja vacia donde en este caso acomodamos los botones.
                                    # .Frame() esta en la libreria de ttk para interfaces graficas
        marco.pack(padx=10, pady=10, fill="both", expand=True)

        for texto, fila, col in botones:
            btn = ttk.Button(marco, text=texto, command=lambda t=texto: self._al_presionar(t))   #pasamos el marco, es el widget donde va a vivir el button
                #t=texto porque sino no imprime lo que esta en el momento, imprime lo ultimo que ve               # No va a vivir en la ventana principal

            btn.grid(row=fila, column=col, sticky="nsew", padx=3, pady=3, ipadx=5, ipady=5)

        # Distribución uniforme
        for i in range(6):  # filas 0‑5
            marco.rowconfigure(i, weight=1)
        for j in range(4):  # columnas 0‑3
            marco.columnconfigure(j, weight=1)

    # ---------- Lógica ---------- #
    def _al_presionar(self, tecla: str):
        if tecla == "C":
            self.expresion = ""
        elif tecla == "=":
            self._evaluar()
        else:
            self.expresion += self._mapear(tecla)
        self._actualizar_display()

    def _mapear(self, tecla: str) -> str:
        """Reemplaza símbolos visuales por operadores de Python."""
        return {                   #diccionario con mapeo personalizado
            "÷": "/",
            "×": "*",
        }.get(tecla, tecla)        #busca si la tecla esta en el diccionario, devuelve lo del dicc, sino devuelve la misma tecla.

    def _evaluar(self):
        try:
            resultado = eval(self.expresion)   #eval() es una funcion de python que evalua str como si fuese codigo py. pegriloso.
            self.expresion = str(resultado)   #convertimos el resultado (numero) de la eval() a str, para poder mostrarlo en el display
        except Exception:
            self.expresion = "Error"

    def _actualizar_display(self): 
        self.display.configure(state="normal")
        self.display.delete(0, tk.END)      # "0" -> primer caracter, "tk.END" -> hasta el final del texto
        self.display.insert(0, self.expresion)
        self.display.configure(state="readonly")


if __name__ == "__main__":    #ejecuta solo si esta siento usado directamente, no importado. Sino correria en el momento que se importa. Ponele
                             # __name__ va a valer "nombredelarchivo" si esta siendo importado. Como importamos tkinter
    app = Calculadora()
    app.mainloop()    #es un metodo de tkinter y lo podemos usar gracias a que la class Calculadora hereda de (tk.Tk)
                        #hace que la ventana quede abierta hasta que la cerremos, esperando cliks.
