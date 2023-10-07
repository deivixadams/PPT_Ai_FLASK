import re
class LimpiaTexto:
    def limpiar_texto(self, texto):
        pattern = re.compile('[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ.,?!¡¿ ]')
        texto_limpio = pattern.sub('', texto)
        return texto_limpio


