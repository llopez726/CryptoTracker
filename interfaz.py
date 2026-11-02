import tkinter as tk
from tkinter import ttk
from api_bitso import obtener_precio
from gestor_datos import inicializar_csv, guardar_registros
from datetime import datetime

class CryptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CryptoTracker Pro - Bitso Monitor")
        self.root.geometry("650x450")
        self.root.config(bg="#1e1e1e")

        # Inicializar base de datos CSV
        inicializar_csv()

        # Lista de criptomonedas a monitorear
        self.pares = [
            {"nombre": "Bitcoin (BTC)", "book": "btc_usd"},
            {"nombre": "Ethereum (ETH)", "book": "eth_usd"},
            {"nombre": "Litecoin (LTC)", "book": "ltc_usd"},
            {"nombre": "Cosmos (ATOM)", "book": "atom_usd"},
            {"nombre": "Dogecoin (DOGE)", "book": "doge_usd"},
            {"nombre": "Ripple (XRP)", "book": "xrp_usd"},
            {"nombre": "Cardano (ADA)", "book": "ada_usd"},
            {"nombre": "TRON (TRX)", "book": "trx_usd"}
        ]
        
        self.precios_anteriores = {}

        # Título de la App
        titulo = tk.Label(root, text="🚀 CryptoTracker Pro", font=("Arial", 18, "bold"), fg="#00ffcc", bg="#1e1e1e")
        titulo.pack(pady=10)

        # Tabla (Treeview) para mostrar los datos
        self.columnas = ("Moneda", "Precio (USD)", "Cambio")
        self.tabla = ttk.Treeview(root, columns=self.columnas, show="headings", height=8)
        
        for col in self.columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor="center", width=180)

        self.tabla.pack(pady=10)

        # Etiqueta de estado / última actualización
        self.lbl_estado = tk.Label(root, text="Estado: Esperando primera actualización...", font=("Arial", 10), fg="#aaaaaa", bg="#1e1e1e")
        self.lbl_estado.pack(pady=5)

        # Botón para actualizar manualmente
        btn_actualizar = tk.Button(root, text="Actualizar Precios Ahora", command=self.actualizar_datos, font=("Arial", 10, "bold"), bg="#00ffcc", fg="#1e1e1e", relief="flat", padx=10, pady=5)
        btn_actualizar.pack(pady=10)

        # Ejecutar la primera actualización y activar el ciclo automático
        self.actualizar_datos()

    def actualizar_datos(self):
        tiempo_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        datos_para_guardar = []
        
        # Limpiar tabla actual
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for cripto in self.pares:
            precio_actual = obtener_precio(cripto["book"])
            
            if precio_actual is not None:
                cambio_str = "— 0.00%"
                
                if cripto["book"] in self.precios_anteriores:
                    precio_anterior = self.precios_anteriores[cripto["book"]]
                    diferencia = precio_actual - precio_anterior
                    
                    if precio_anterior > 0:
                        porcentaje = (diferencia / precio_anterior) * 100
                        if porcentaje > 0:
                            cambio_str = f"▲ +{porcentaje:.2f}%"
                        elif porcentaje < 0:
                            cambio_str = f"▼ {porcentaje:.2f}%"
                
                self.precios_anteriores[cripto["book"]] = precio_actual
                
                # Insertar fila en la tabla gráfica
                self.tabla.insert("", "end", values=(cripto["nombre"], f"${precio_actual:,.4f}", cambio_str))
                
                # Preparar datos para el CSV
                datos_para_guardar.append(f"{tiempo_actual},{cripto['nombre']},{precio_actual}\n")
            else:
                self.tabla.insert("", "end", values=(cripto["nombre"], "Error de conexión", "N/A"))

        # Guardar registros en el CSV histórico
        if datos_para_guardar:
            guardar_registros(datos_para_guardar)

        self.lbl_estado.config(text=f"Última actualización: {tiempo_actual}")

        # Programar la siguiente actualización automática en 10 segundos (10000 milisegundos)
        self.root.after(10000, self.actualizar_datos)

if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoApp(root)
    root.mainloop()