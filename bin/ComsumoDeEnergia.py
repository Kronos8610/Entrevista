import requests  # Importa la librería para hacer solicitudes HTTP
import json      # Importa la librería para trabajar con datos JSON

# Función para obtener las temperaturas de Open Meteo a partir de la latitud y longitud
def obtener_temperaturas_open_meteo(latitud, longitud):
    # Construye la URL para la API de Open Meteo con los parámetros de latitud y longitud
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitud}&longitude={longitud}&hourly=temperature_2m"
    
    # Realiza la solicitud GET a la API
    respuesta = requests.get(url)
    
    # Convierte la respuesta en formato JSON
    datos = respuesta.json()

    # Si la solicitud fue exitosa (status code 200)
    if respuesta.status_code == 200:
        # Obtiene las temperaturas horarias para los próximos días (cada 2 metros de altura)
        temperaturas_horarias = datos["hourly"]["temperature_2m"]

        # Divide las temperaturas horarias en bloques de 24 para cada día
        temperaturas_diarias = [temperaturas_horarias[i:i + 24] for i in range(0, len(temperaturas_horarias), 24)]

        # Lista de días de la semana para asignar las temperaturas a cada día
        dias = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]

        # Crea un diccionario que asocia los días de la semana con las temperaturas diarias
        temperaturas = dict(zip(dias, temperaturas_diarias))

        # Retorna el diccionario con las temperaturas diarias por día
        return temperaturas
    else:
        # Si no se pudo obtener la respuesta correctamente, retorna None
        return None

# Función para calcular el consumo de energía basado en las temperaturas diarias
def calcular_consumo(temperaturas):
    # Obtiene los días de la semana del diccionario de temperaturas
    dias = list(temperaturas.keys())
    resultados = []  # Lista para almacenar los resultados de consumo de energía por día

    # Recorre cada día y sus temperaturas horarias
    for dia in dias:
        # Obtiene las temperaturas horarias para el día
        temperaturas_horarias = temperaturas[dia]

        # Calcula la temperatura media diaria (TMD) sumando las temperaturas horarias y dividiendo por la cantidad de horas (24)
        TMD = sum(temperaturas_horarias) / len(temperaturas_horarias)

        # Calcula el consumo de energía como la diferencia entre 15°C y la TMD. Si es negativo, se establece en 0.
        consumo_energia = max(0, (15 - TMD))

        # Crea un diccionario con los resultados del día: nombre del día, TMD, temperaturas horarias y consumo de energía
        resultado = {
            "dia": dia,
            "TMD": TMD,
            "temperaturas_horarias": temperaturas_horarias,
            "consumo_energia": consumo_energia
        }

        # Añade el resultado del día a la lista de resultados
        resultados.append(resultado)

    # Retorna la lista con todos los resultados de consumo por día
    return resultados

# Función para guardar los resultados en un archivo JSON
def guardar_resultados(resultados):
    # Abre (o crea) un archivo llamado 'consumo_energia.json' en modo escritura
    with open('consumo_energia.json', 'w') as archivo:
        # Convierte la lista de resultados a formato JSON y la guarda en el archivo, con indentación para mejorar la legibilidad
        json.dump(resultados, archivo, indent=4)

# Coordenadas geográficas (latitud y longitud) para Madrid
latitud = 40.4168
longitud = -3.7038

# Obtiene las temperaturas de Open Meteo para la ubicación dada
temperaturas = obtener_temperaturas_open_meteo(latitud, longitud)

# Si las temperaturas fueron obtenidas correctamente
if temperaturas is not None:
    # Calcula el consumo de energía basado en las temperaturas obtenidas
    resultados = calcular_consumo(temperaturas)
    
    # Guarda los resultados en un archivo JSON
    guardar_resultados(resultados)

    # Imprime los resultados por consola
    for resultado in resultados:
        print(f"Día: {resultado['dia']}")
        print(f"TMD: {resultado['TMD']}")
        print(f"Temperaturas horarias: {resultado['temperaturas_horarias']}")
        print(f"Consumo de energía: {resultado['consumo_energia']}\n")
else:
    # Si no se pudieron obtener las temperaturas, imprime un mensaje de error
    print("No se pudieron obtener las temperaturas.")
