

from models.presentation_creator import PresentationCreator
from models.info_converter import InfoConverter
from models.openai_langchain import OpenAiLC
#from models.web_reader import WebReader
from models.text_cleaner import LimpiaTexto
from langchain.chains import LLMChain
#from langchain import PromptTemplate
from langchain.prompts import PromptTemplate
import logging

#, ExtractorTextoPDF, InfoConverter, openai_langchain, WebReader

class Application:
    def __init__(self):
        #2---instanciamos las clases que necesitamos
        self.presentation_creator = PresentationCreator() # Create an instance of the PresentationCreator class
        #self.pdf_reader = LeerPDF() # Create an instance of the LeerPDF class
        #self.texto_presentacion = TextoPresentacion(api_key=tools.API_KEY)  # Replace with actual API_KEY or a way to input it.
        #self.info_converter = InfoConverter() # Create an instance of the InfoConverter class
        self.llmlc = OpenAiLC() #  en old code: openai_langchain / Create an instance of the openai_langchain class
        #self.web_reader = WebReader() # Create an instance of the WebReader class
        #nota: la de pdf la instancion en el metodo pdf_a_presentacion
        

    '''
    PARTE 1 - [{PROMPT PARA LLM A TRAVES DE LANGCHAIN}]
    '''
    def PromptLC_Text2ppt(self, datagpt):
        try:
            print(f"CANTIAD ES--->{datagpt['cantidad']}")
            #pause = input("Vise la cantidad de parrafos")
            prompt = PromptTemplate(
                input_variables=["tema", "cantidad", "palabras"],
                template='''
                    Sobre este tema {tema}.
                    Genera una cantidad de parrafo igual a {cantidad}. máximo {palabras} palabras por parrafo.
                    Salida diccionario de python por cada parrafo. Colocar los diccionarios en una lista de python con el siguiente formato:
                    "title": aquí debes generar un titulo acorde al parrafo, "content": "aquí colocar el parrafo"
                '''
            )
            logging.debug(f"prompt--->: {prompt}")
            cadena = LLMChain(llm=self.llmlc.openai_lc(), prompt=prompt)
            return cadena.run(datagpt)
        except Exception as e:
            print(f"Error en PromptLC_Text2ppt: {e}")
            return {"error": str(e)}


    #----------------dataweb--------------------------------
    def PromptLC_Web2ppt(self, dataweb):
        prompt = PromptTemplate(
            input_variables=["tema", "tono"],
            template='''
                Hacer un resumen de {tema} en este tono: {tono}. máximo {self.cantidad_pal_parrafos} palabras por parrafo.
                Salida un diccionario de python por cada parrafo. Colocar los diccionarios en una lista de python con el siguiente formato:
                "title": aquí debes generar un titulo acorde al parrafo, "content": "aquí colocar el parrafo"
            '''
        )
        
        cadena = LLMChain(llm=self.llmlc.openai_lc(), prompt=prompt)
        return cadena.run(dataweb)


    #----------------dataPDF--------------------------------
    def PromptLC_PDF2ppt(self, datapdf):
        prompt = PromptTemplate(
            input_variables=["tema"],
            template='''
                Hacer un resumen en español del {tema}. máximo {self.cantidad_pal_parrafos} palabras por parrafo.
                Salida un diccionario de python por cada parrafo. Colocar los diccionarios en una lista de python con el siguiente formato:
                "title": aquí debes generar un titulo acorde al parrafo, "content": "aquí colocar el parrafo"
            '''
        )
        
        cadena = LLMChain(llm=self.llmlc.openai_lc(), prompt=prompt)
        return cadena.run(datapdf)







