import time
from datetime import datetime
from api_bitso import obtener_precio
from gestor_datos import inicializar_csv, guardar_registros, verificar_alerta

def ejecutar_monitor():
    pares = [
        {"nombre": "Bitcoin (BTC)", "book": "btc_usd"},
        {"nombre": "Ethereum (ETH)", "book": "eth_usd"},
        {"nombre": "Litecoin (LTC)", "book": "ltc_usd"},
        {"nombre": "Cosmos (ATOM)", "book": "atom_usd"},
        {"nombre": "Dogecoin (DOGE)", "book": "doge_usd"},
        {"nombre": "Ripple (XRP)", "book": "xrp_usd"},
        {"nombre": "Cardano (ADA)", "book": "ada_usd"},
        {"nombre": "TRON (TRX)", "book": "trx_usd"}
    ]
    
    precios_anteriores = {}
    inicializar_csv()
    
    print("Iniciando CryptoTracker con Alertas Inteligentes. Presiona Ctrl + C para salir...\n")
    
    while True:
        tiempo_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"================ [{tiempo_actual}] ================")
        
        datos_para_guardar = []
        
        for cripto in pares:
            precio_actual = obtener_precio(cripto["book"])
            
            if precio_actual is not None:
                cambio_str = ""
                porcentaje = 0.0
                
                if cripto["book"] in precios_anteriores:
                    precio_anterior = precios_anteriores[cripto["book"]]
                    diferencia = precio_actual - precio_anterior
                    
                    if precio_anterior > 0:
                        porcentaje = (diferencia / precio_anterior) * 100
                        if porcentaje > 0:
                            cambio_str = f" (▲ +{porcentaje:.2f}%)"
                        elif porcentaje < 0:
                            cambio_str = f" (▼ {porcentaje:.2f}%)"
                        else:
                            cambio_str = " (— 0.00%)"
                        
                        # Evaluamos si el movimiento supera el umbral para lanzar alerta
                        verificar_alerta(cripto["nombre"], porcentaje)
                
                precios_anteriores[cripto["book"]] = precio_actual
                print(f"-> {cripto['nombre']}: ${precio_actual:,.4f} USD{cambio_str}")
                
                datos_para_guardar.append(f"{tiempo_actual},{cripto['nombre']},{precio_actual}\n")
            else:
                print(f"-> No se pudo obtener el precio de {cripto['nombre']}.")
                
        guardar_registros(datos_para_guardar)
            
        print("\n[Datos guardados en CSV]")
        print("Esperando 10 segundos para la próxima actualización...\n")
        time.sleep(10)

if __name__ == "__main__":
    ejecutar_monitor()