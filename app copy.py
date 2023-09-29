from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', title='MyWebApp')

@app.route('/txt2ppt', methods=['POST', 'GET'])  
def txt2ppt():
    if request.method == 'POST':
        data = request.json
        tema = data.get('tema')
        cantidad = data.get('cantidad')
        datos_recibidos = {"tema": tema, "cantidad": cantidad}
        
        # Renderizar la plantilla con los datos recibidos
        return render_template('mostrar_datos.html', datos=datos_recibidos) 
        
    return render_template('txt2ppt.html')

@app.route('/pdf_a_presentacion')
def pdf_a_presentacion():
    return '¡Aquí puedes convertir PDF a presentación!'

@app.route('/web_a_presentacion')
def web_a_presentacion():
    return '¡Aquí puedes convertir web a presentación!'



#-------------------FUNCIONES CLAVES-------------------#
def PromptLC_Web2ppt(self, dataweb):
    prompt = PromptTemplate(
        input_variables=["tema", "tono"],
        template='''
            Hacer un resumen de {tema} en este tono: {tono}. máximo 70 palabras por parrafo.
            Salida un diccionario de python por cada parrafo. Colocar los diccionarios en una lista de python con el siguiente formato:
            "title": aquí debes generar un titulo acorde al parrafo, "content": "aquí colocar el parrafo"
        '''
    )
    
    cadena = LLMChain(llm=self.llmlc.openai_lc(), prompt=prompt)
    return cadena.run(dataweb)

if __name__ == '__main__':
    app.run(debug=True)
