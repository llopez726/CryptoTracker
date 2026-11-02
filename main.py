import time
import requests

def consultar_bitso_en_dolares():
    pares = [
        {"nombre": "Cosmos (ATOM)", "book": "atom_usd"},
        {"nombre": "Dogecoin (DOGE)", "book": "doge_usd"},
        {"nombre": "Ripple (XRP)", "book": "xrp_usd"},
        {"nombre": "Cardano (ADA)", "book": "ada_usd"},
        {"nombre": "TRON (TRX)", "book": "trx_usd"}
    ]
    
    print("Iniciando monitor de criptomonedas (Presiona Ctrl + C para salir)...\n")
    
    # Un ciclo infinito para que se repita constantemente
    while True:
        print("--------------------------------------------------")
        print("Actualizando precios...")
        
        for cripto in pares:
            url = f"https://api.bitso.com/v3/ticker/?book={cripto['book']}"
            
            try:
                respuesta = requests.get(url, timeout=5)
                
                if respuesta.status_code == 200:
                    datos = respuesta.json()
                    precio = datos["payload"]["last"]
                    print(f"-> {cripto['nombre']}: ${float(precio):,.4f} USD")
                else:
                    print(f"-> No se encontró el par para {cripto['nombre']}.")
                    
            except Exception as e:
                print(f"Error de red con {cripto['nombre']}: {e}")
        
        print("Esperando 10 segundos para la próxima actualización...\n")
        # El programa pausará aquí durante 10 segundos antes de volver a consultar
        time.sleep(10)

if __name__ == "__main__":
    consultar_bitso_en_dolares()
