from flask import Flask, render_template, url_for, redirect, flash, session, request
import bcrypt
import database as dbase
from funciones import nocache, obtener_documentos_alumno_uta, obtener_usuario_por_correo
from create import init_create
from update import init_update
from view import init_view
db = dbase.dbConnection()
app = Flask(__name__)
init_create(app)

init_update(app)
init_view(app)
app.secret_key = 'M0i1Xc$GfPw3Yz@2SbQ9lKpA5rJhDtE7'
app.config['SESSION_COOKIE_NAME'] = 'session_admin'

@app.route('/')
@nocache
def Home():    
    return render_template ('Main.html')

@app.route('/EduLink/login/')
def login():
    return render_template('login.html')


    
@app.route('/EduLink/registro/')
def registro():
    carreras = db['carreras'].find()
    periodos=db['Periodos'].find()
    return render_template('registro.html',Carreras = carreras, Periodos=periodos)
    
@app.route('/iniciar/', methods=['POST'])
def iniciar():
    correo = request.form['correo']
    password = request.form['password']
    alumno = db['usuarios']

        
    login_alumno = alumno.find_one({'correoAlumno': correo})
    if login_alumno and bcrypt.checkpw(password.encode('utf-8'), login_alumno['contraseñaAlumno']):
            # Autenticación exitosa
            session['correo'] = correo
            flash('Inicio de sesión exitoso como alumno.','success')
            return redirect(url_for('alumno_vista'))    

    # Si el inicio de sesión falla, muestra un mensaje de error
    flash('Correo o contraseña incorrectos', 'danger')
    return redirect(url_for('login'))

            
@app.route('/EduLink/Alumno/')
@nocache
def alumno_vista():
    correo = session.get('correo')
    if correo:
        alumno = obtener_usuario_por_correo(correo)
        if alumno:
            documentacion_alumno = obtener_documentos_alumno_uta(alumno['_id'])

            # Obtener la lista de carreras y periodos
            carreras = list(db['carreras'].find())
            periodos = list(db['Periodos'].find())

            # Convertir carreras y periodos a diccionarios con _id como clave
            carreras_dict = {str(carrera['_id']): carrera['NombreCarrera'] for carrera in carreras}
            periodos_dict = {str(periodo['_id']): {'NombrePeriodo': periodo['NombrePeriodo'], 'Duracion': periodo['Duracion']} for periodo in periodos}

            # Asignar el nombre de la carrera y del periodo al alumno actual
            alumno['NombreCarrera'] = carreras_dict.get(alumno.get('idCarrera', ''), 'Carrera no encontrada')
            periodo_info = periodos_dict.get(alumno.get('idPeriodo', ''), {'NombrePeriodo': 'Periodo no encontrado', 'Duracion': ''})
            alumno['NombrePeriodo'] = periodo_info['NombrePeriodo']
            alumno['Duracion'] = periodo_info['Duracion']

            return render_template('alumno_uta.html', alumno=alumno, documentos=documentacion_alumno, Carreras=carreras, Periodos=periodos)
        else:
            flash('No se encontró al alumno.', 'danger')
    return redirect(url_for('login'))



@app.route("/EduLink/Alumno/Archivos_Universidad/")
@nocache
def catalago():
    if 'correo' in session:
        conexion = db['archivos_vinculacion']
        archivos = list(conexion.find())  # Convertir el cursor a una lista de documentos
        for archivo in archivos:
            archivo['extension'] = archivo['nombre'].split('.')[-1].lower()  # Obtener la extensión de cada archivo
        return render_template("Archivos_uta.html", archivos=archivos)
    else:
     flash('Acceso denegado: Debes de inciar sesion.', 'danger')
     return redirect(url_for('login'))



########LOGOUT############

@app.route('/logout', methods=['POST'])
@nocache
def logout():
    session.clear()  # Elimina todas las variables de sesión
    return redirect(url_for('login'))  # Redirige al inicio de sesión

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

if __name__ == '__main__':

    app.run(debug=True,host='0.0.0.0', port=8000)
