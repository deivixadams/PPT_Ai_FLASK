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
    if request.method == 'POST':
        data = request.json
        tema = data.get('tema')
        cantidad = data.get('cantidad')
        
        datatxt = {'tema': tema, 'cantidad': cantidad}  # Ajusta según sea necesario.
        
        response = tools_instance.PromptLC_Text2ppt(datatxt)
        
        dataslide = info_converter.convertir_info(response)  # Actualiza dataslide con la respuesta
        
        creador_presentacion.crear_presentacion(dataslide)
        
    return render_template('txt2ppt.html', dataslide=dataslide)  # Pasa dataslide a la plantilla


#para bajar el archivo ppt creado
@app.route('/usar_texto', methods=['POST'])
def usar_texto():
    dataslide = request.get_json()
    ruta_archivo = creador_presentacion.crear_presentacion(dataslide)
    if ruta_archivo:
        # Extrae el nombre del archivo de la ruta del archivo
        nombre_archivo = os.path.basename(ruta_archivo)
        return jsonify({"success": True, "ruta_descarga": url_for('descargas', filename=nombre_archivo)})
    else:
        return jsonify({"success": False, "error": "No se pudo crear la presentación."})

'''
@app.route('/list_presentations')
def list_presentations():
    directory = "RESULTADO"
    files = [f for f in os.listdir(directory) if f.endswith('.pptx')]
    return render_template('list_presentations.html', files=files)
'''

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
