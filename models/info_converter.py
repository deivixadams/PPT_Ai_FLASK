import json

class InfoConverter:
    def convertir_info(self, dataslide):
        #print(f"info es-------------->: {info}")
        if isinstance(dataslide, dict):  # Verifica si dataslide ya es un diccionario
            return dataslide  # Retorna el diccionario directamente si es el caso
        try:
            return json.loads(dataslide)  # Intenta parsear como JSON si info es una cadena
        except json.JSONDecodeError:
            print("La cadena no está en un formato JSON válido.")
        except TypeError:
            print("El objeto a convertir debe ser una cadena, bytes o bytearray.")
