

'''
import re
import re
import openai
import json
import json
import requests
from bs4 import BeautifulSoup
import fitz  # fitz es el módulo principal de PyMuPDF
from langchain.chat_models import ChatOpenAI
'''


import os
from pptx import Presentation
from pptx.util import Inches
from datetime import datetime


class PresentationCreator:

    def crear_presentacion(self, info):
        #infojson = self.convertir_info(info)
        #print("Creando presentación...\n")
        prs = Presentation()
        ahora = datetime.now()
        fecha_hora = ahora.strftime("fecha-%d-%m-%Y_hora-%H-%M-%S")
        
        for slide_info in info:
            slide_layout = prs.slide_layouts[5]
            slide = prs.slides.add_slide(slide_layout)
            title_box = slide.shapes.title
            title_box.text = slide_info["title"]
            left = Inches(1)
            top = Inches(1.5)
            width = height = Inches(6)
            txBox = slide.shapes.add_textbox(left, top, width, height)
            tf = txBox.text_frame
            p = tf.add_paragraph()
            p.text = slide_info["content"]
        
        nombre_archivo = f"{fecha_hora}.pptx"
        ruta_guardado = os.path.join("RESULTADO", nombre_archivo)
        try:
            prs.save(ruta_guardado)
            if os.path.exists(ruta_guardado):
                (f"He creado el archivo:{fecha_hora} \n")
        except PermissionError:
            print("No se pudo crear el archivo, probablemente esté abierto.")


