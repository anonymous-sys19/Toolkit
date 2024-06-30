import requests
import os
import json
from dotenv import load_dotenv
import sys

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

def dns_lookup(domain):
    """
    Realiza una búsqueda DNS utilizando la API de API Ninjas y devuelve la respuesta en formato JSON.
    """
    api_key = os.getenv("API_KEY")
    if not api_key:
        print("API key no encontrada. Asegúrate de que está definida en tu archivo .env.")
        return

    if not domain:
        print("El dominio no puede estar vacío.")
        return

    api_url = f'https://api.api-ninjas.com/v1/dnslookup?domain={domain}'

    try:
        response = requests.get(api_url, headers={"X-Api-Key": api_key})
        response.raise_for_status()  # Lanza una excepción para códigos de estado HTTP 4xx/5xx

        # Decodificar la respuesta JSON
        response_json = response.json()
        one_line_json = json.dumps(response_json, indent=2)
        pretty_json = json.dumps(response_json, indent=2)

        # Imprimir los resultados
        print(f'Original: {one_line_json}')
        print(f'Pretty: {pretty_json}')

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Error occurred: {req_err}")
    except json.JSONDecodeError as json_err:
        print(f"JSON decode error: {json_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        dns_lookup(sys.argv[1])
    else:
        print("Usage: dns_lookup.py <DOMAIN>")
