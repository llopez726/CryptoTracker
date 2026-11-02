from datetime import datetime

ARCHIVO_CSV = "historial_precios.csv"

def inicializar_csv():
    try:
        with open(ARCHIVO_CSV, "x", encoding="utf-8") as f:
            f.write("Fecha_Hora,Moneda,Precio_USD\n")
    except FileExistsError:
        pass

def guardar_registros(datos_a_guardar):
    with open(ARCHIVO_CSV, "a", encoding="utf-8") as f:
        f.writelines(datos_a_guardar)

def verificar_alerta(nombre_moneda, porcentaje):
    # Umbral de alerta (por ejemplo, un cambio mayor o igual al 0.1% en un ciclo)
    UMBRAL = 0.1 
    
    if porcentaje >= UMBRAL:
        print(f"🚨 ¡ALERTA DE ALZA! 🚀 {nombre_moneda} subió un +{porcentaje:.2f}%")
    elif porcentaje <= -UMBRAL:
        print(f"🚨 ¡ALERTA DE BAJA! 📉 {nombre_moneda} cayó un {porcentaje:.2f}%")