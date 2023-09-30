from flask import Flask, render_template, request, jsonify, send_from_directory, abort, redirect, url_for
from models.tools import Application
from models.info_converter import InfoConverter
from models.presentation_creator import PresentationCreator
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore

from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin

from flask_migrate import Migrate
from flask_security.decorators import roles_required
from flask_login import current_user
from datetime import datetime
import os


app = Flask(__name__)

#-----------------Configuraciones Seguridad-----------------
# Configuración adicional de Flask-Security y SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Esto creará test.db en el mismo directorio que app.py
app.config['SECRET_KEY'] = 'super-secret'  # Cambia esto por una clave secreta real
app.config['SECURITY_REGISTERABLE'] = True  # Permite el registro de usuarios
app.config['SECURITY_PASSWORD_SALT'] = '22716652dab05d88202f5a66d9a35d38df2ace926b7491420f3b19d2aac108de5782bbe4f7df01f882082db123953d420fc6ae779fa499b9d7e89c641fdb5000'
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
app.config['SECURITY_CONFIRMABLE'] = False
app.config['SECURITY_RECOVERABLE'] = False
app.config['SECURITY_LOGIN_USER_TEMPLATE'] = 'security/login.html'
app.config['SECURITY_REGISTER_USER_TEMPLATE'] = 'security/register.html'



# Inicializa SQLAlchemy
db = SQLAlchemy(app)

# Inicializa Flask-Migrate
migrate = Migrate(app, db)


# Define el modelo Role
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)

# Define el modelo User
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    expires_at = db.Column(db.DateTime())  # Fecha de expiración del acceso
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary='user_roles')

# Define la tabla asociativa user_roles
class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

# Configura Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, datastore=user_datastore)




#-----------------instanciamos las clases-----------------
# Crea una instancia de Application
tools_instance = Application() 
info_converter = InfoConverter()
creador_presentacion = PresentationCreator()


#-----------------rutas-----------------
@app.route('/')
def home():
    return render_template('index.html', title='MyWebApp')


@app.route('/admin')
@roles_required('admin') # Solo los usuarios con el rol 'admin' pueden acceder a esta ruta
def admin_home():
    return "Admin Home"

#esto hace que no se requiera autenticación para las rutas que se encuentran en la lista
ANONYMOUS_ACCESS_ROUTES = [
    'security.login',
    'security.register',
    # Añade aquí cualquier otra ruta que quieras permitir el acceso anónimo
]

#Esto hace que se requiera autenticación para todas las rutas
@app.before_request
def require_login_and_check_expiration():
    # Si la ruta actual está en la lista de acceso anónimo, retorna y no hagas nada.
    if request.endpoint in ANONYMOUS_ACCESS_ROUTES:
        return
    
    # Si el usuario actual no está autenticado, redirige al usuario a la página de login.
    if not current_user.is_authenticated:
        return redirect(url_for('security.login'))
    
    # Si el usuario actual está autenticado pero su acceso ha expirado, retorna un error 403.
    if current_user.expires_at and current_user.expires_at < datetime.utcnow():
        abort(403, description="Access expired.")


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
