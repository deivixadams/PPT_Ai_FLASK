from flask import Flask, render_template, request, jsonify
from models.tools import Application  # Ajusta la importación para reflejar la estructura de directorios
from models.info_converter import InfoConverter
from models.presentation_creator import PresentationCreator 


app = Flask(__name__)

#-----------------instanciamos las clases-----------------
# Crea una instancia de Application
tools_instance = Application() 
info_converter = InfoConverter()
creador_presentacion = PresentationCreator()


#-----------------rutas-----------------
@app.route('/')
def home():
    return render_template('index.html', title='MyWebApp')

@app.route('/txt2ppt', methods=['POST', 'GET'])  
def txt2ppt():
    if request.method == 'POST':
        data = request.json
        tema = data.get('tema')
        cantidad = data.get('cantidad')
        
        datatxt = {'tema': tema, 'cantidad': cantidad}  # Ajusta según sea necesario.
        #print(f"LA CANTIDAD ES-------------->: {datatxt}")
        response = tools_instance.PromptLC_Text2ppt(datatxt)
        
        dataslide = info_converter.convertir_info(response)
        #dataslide = list(dataslide)[:cantidad] # convertir a lista y tomar los primeros slides
        
        #print(dataslide)

        creador_presentacion.crear_presentacion(dataslide)
        
        return jsonify(response)  # Asumiendo que la respuesta puede ser serializada a JSON.
        
    return render_template('txt2ppt.html')


@app.route('/pdf_a_presentacion')
def pdf_a_presentacion():
    return '¡Aquí puedes convertir PDF a presentación!'

@app.route('/web_a_presentacion')
def web_a_presentacion():
    return '¡Aquí puedes convertir web a presentación!'


if __name__ == '__main__':
    app.run(debug=True)
