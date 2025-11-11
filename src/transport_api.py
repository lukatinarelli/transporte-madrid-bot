import requests

def get_bus_times(stop_id: str):
    """
    Consulta la API de CTRM para una parada concreta y devuelve los tiempos de llegada de los buses.
    :param stop_id: ID de la parada (string)
    :return: Lista de diccionarios con bus y tiempo
    """
    url = f"https://api.ctm-madrid.es/endpoint_paradas/{stop_id}"  # Cambiar al endpoint real
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Procesamos los datos según cómo venga la API
        buses = []
        for bus in data.get("buses", []):
            buses.append({
                "line": bus["linea"],
                "destination": bus["destino"],
                "time": bus["tiempo_llegada"]
            })
        return buses

    except requests.RequestException as e:
        print(f"Error consultando la API: {e}")
        return []
