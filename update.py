from bson import  Binary, ObjectId
from flask import flash, redirect,  request, url_for
import database as dbase
from funciones import subir_documento
db = dbase.dbConnection()
from bson import ObjectId


def init_update(app):


    
    @app.route('/subir_Documento_uta/', methods=['POST'])#####Alumno
    def subir_documento_alumno_uta():
        id_alumno = request.form.get('id_alumno')
        alumno = db['usuarios'].find_one({'_id':ObjectId(id_alumno)})
        archivo = request.files['archivo']
        if alumno:
            if archivo:
                if archivo.filename.endswith('.pdf'):
                    archivo_data = archivo.read()
                    archivo_bin = Binary(archivo_data)
                    
                    # Actualiza el documento del alumno
                    db['usuarios'].update_one(
                        {'_id': ObjectId(id_alumno)},
                        {'$set': {
                            'formato_tres_opciones.estado':'entregado',
                            'formato_tres_opciones.archivo': archivo_bin}}
                    )
                    flash('Documento subido exitosamente', 'success')
                else:
                    flash('El archivo debe ser .pdf', 'warning')
            else:
                flash('No se ha seleccionado ningún archivo', 'warning')
        else:
            flash('Alumno no encontrado en la base de datos', 'danger')
        
        return redirect(url_for('alumno_vista', id_alumno=id_alumno))

    
    @app.route('/subir_documento_alumo/<id_alumno>/<documento_nombre>', methods=['GET', 'POST'])########alumno
    def subir_documento_uta(id_alumno, documento_nombre):
        if request.method == 'POST':
            archivo = request.files['archivo']
            if subir_documento(id_alumno, documento_nombre, archivo):
                flash('Documento subido exitosamente.', 'success')
            else:
                flash('No se pudo subir el documento. Inténtelo de nuevo.', 'danger')
            return redirect(url_for('alumno_vista', id_alumno=id_alumno))
        return redirect(url_for('alumno_vista', id_alumno=id_alumno))