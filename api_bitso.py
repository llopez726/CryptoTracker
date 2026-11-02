import requests

def obtener_precio(book):
    url = f"https://api.bitso.com/v3/ticker/?book={book}"
    try:
        respuesta = requests.get(url, timeout=5)
        if respuesta.status_code == 200:
            datos = respuesta.json()
            return float(datos["payload"]["last"])
    except Exception as e:
        print(f"Error al consultar {book}: {e}")
    return None