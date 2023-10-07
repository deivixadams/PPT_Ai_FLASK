
import os
import logging
from pywinauto import Application
import psutil
import time
import pyautogui

# Configurar el logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PttxDesign:

    def __init__(self, ruta_archivo, cantidad_slides):
        self.ruta_archivo = ruta_archivo
        self.cantidad_slides = cantidad_slides

    # Cerrando PowerPoint
    def cerrar_powerpoint(self):
        try:
            for proceso in psutil.process_iter(['pid', 'name']):
                if proceso.info['name'] == 'POWERPNT.EXE':
                    proceso.terminate()
                    time.sleep(2)

            # Verificar si todas las instancias de PowerPoint fueron cerradas
            powerpoint_procesos = [proceso for proceso in psutil.process_iter(['pid', 'name']) if proceso.info['name'] == 'POWERPNT.EXE']
            if not powerpoint_procesos:
                logging.info("Todas las instancias de PowerPoint fueron cerradas con éxito.")
                return True  # Todas las instancias de PowerPoint fueron cerradas con éxito
            else:
                logging.warning(f"Aún hay {len(powerpoint_procesos)} instancias de PowerPoint en ejecución.")
                return False  # Algunas instancias de PowerPoint aún están en ejecución
        except Exception as e:
            logging.error(f"Error en cerrar_powerpoint: {e}")
            return False

    def aplicar_diseño(self):
        # Cerrar PowerPoint si está abierto
        if not self.cerrar_powerpoint():
            logging.error("No se pudo cerrar PowerPoint. El proceso puede estar en ejecución en segundo plano.")
            return False
        
        try:
            # Obtén la ruta al archivo de PowerPoint
            file_path = self.ruta_archivo

            # Abrir el archivo de PowerPoint usando la interfaz de línea de comandos de PowerPoint
            app = Application().start(rf'C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE /o "{file_path}"')

            # Esperar a que PowerPoint esté completamente cargado (ajustar el tiempo según sea necesario)
            ppt_window = app.window(title_re=".*PowerPoint")
            ppt_window.wait('ready', timeout=40)
            # Maximizar la ventana de PowerPoint
            ppt_window.maximize()


        except Exception as e:
            logging.error(f"Error en aplicar_diseño parte 1: {e}")

        try:
            # Asegúrate de estar en la primera diapositiva antes de empezar a recorrer las diapositivas
            for _ in range(self.cantidad_slides):
                pyautogui.press('up')  # Presionar la flecha arriba varias veces podría llevarnos a la primera diapositiva
                time.sleep(0.5)  # Ajusta este tiempo de espera según sea necesario

            for slide_number in range(1, self.cantidad_slides + 1):
                # Ya que estamos en la primera diapositiva, solo necesitamos avanzar a la siguiente diapositiva
                if slide_number > 1:
                    pyautogui.press('derecha')  # Presionar la flecha derecha para avanzar a la siguiente diapositiva
                    time.sleep(3)  # Ajusta este tiempo de espera según sea necesario
                    # Navegar a la pestaña Design y abrir el diseñador
                    pyautogui.hotkey('alt', 'g')  # Suponiendo que Alt + G abre la pestaña Design
                    time.sleep(3)
                    pyautogui.hotkey('d')  
                    time.sleep(3)
                    pyautogui.hotkey('enter') 
                    time.sleep(3)

        except Exception as e:
            logging.error(f"Error en aplicar_diseño parte 2 (pyautogui): {e}")

        try:
            # Navegar al menú Archivo y seleccionar Guardar
            pyautogui.hotkey('alt', 'f')  # Presionar Alt + F para abrir el menú Archivo
            time.sleep(1)  # Esperar un momento para asegurarse de que el menú esté abierto
            pyautogui.press('s')  # Presionar 's' para seleccionar Guardar
            logging.info("Diseño aplicado y presentación guardada con éxito.")
            return True
        except Exception as e:
            logging.error(f"Error al intentar guardar la presentación: {e}")
            return False

if __name__ == "__main__":
    ruta_archivo = r"D:\AI\INFOTEP_3CASOS\PPT_Ai_FLASK\RESULTADO\5.pptx"
    cantidad_slides = 5  # Suponiendo que hay 2 diapositivas
    design_applicator = PttxDesign(ruta_archivo, cantidad_slides)
    design_applicator.aplicar_diseño()
