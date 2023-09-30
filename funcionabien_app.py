from flask import Flask, render_template, request, jsonify
from models.tools import Application  # Ajusta la importación para reflejar la estructura de directorios
from models.info_converter import InfoConverter
from models.presentation_creator import PresentationCreator 
from flask import send_from_directory
import os


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
    dataslide = []  # Asegúrate de que dataslide esté definido
    mensaje = None  # Inicializa mensaje con None

    if request.method == 'POST':
        data = request.json
        tema = data.get('tema')
        cantidad = data.get('cantidad')
        
        datatxt = {'tema': tema, 'cantidad': cantidad}  # Ajusta según sea necesario.
        
        response = tools_instance.PromptLC_Text2ppt(datatxt)
        
        dataslide = info_converter.convertir_info(response)  # Actualiza dataslide con la respuesta
        #creador_presentacion.crear_presentacion(dataslide)
        
        if dataslide is None:
            mensaje = "Error: No se pudo crear la presentación porque 'dataslide' es None"
            return jsonify({'mensaje': mensaje})
        
        ruta_guardado = creador_presentacion.crear_presentacion(dataslide, tema)
        if ruta_guardado:  # Si la ruta de guardado existe, la creación fue exitosa.
            mensaje = '¡Presentación creada! Puede descargarla en la página de "Listado de presentaciones".'
        else:  # Si la ruta de guardado es None, hubo un error.
            mensaje = 'Hubo un error al crear la presentación.'
        return jsonify({'mensaje': mensaje})  # Devuelve un JSON con el mensaje

    #return render_template('txt2ppt.html', dataslide=dataslide, mensaje=mensaje)  # Pasa dataslide a la plantilla
    return render_template('txt2ppt.html',  mensaje=mensaje)  # Pasa dataslide a la plantilla


@app.route('/list_presentations')
def list_presentations():
    directory = "RESULTADO"
    
    # Lista todos los archivos .pptx en el directorio
    files = [f for f in os.listdir(directory) if f.endswith('.pptx')]
    
    # Obtiene la ruta completa de los archivos
    full_paths = [os.path.join(directory, f) for f in files]
    
    # Ordena los archivos por fecha de creación en modo descendente
    sorted_files = sorted(full_paths, key=os.path.getctime, reverse=True)
    
    # Obtiene solo los nombres de los archivos, no la ruta completa
    sorted_filenames = [os.path.basename(f) for f in sorted_files]
    
    return render_template('list_presentations.html', files=sorted_filenames)



@app.route('/descargas/<filename>')
def descargas(filename):
    return send_from_directory('RESULTADO', filename)

@app.route('/pdf_a_presentacion')
def pdf_a_presentacion():
    return '¡Aquí puedes convertir PDF a presentación!'

@app.route('/web_a_presentacion')
def web_a_presentacion():
    return '¡Aquí puedes convertir web a presentación!'


if __name__ == '__main__':
    app.run(debug=True)
