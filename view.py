import io
from bson import Binary, ObjectId
from flask import flash, redirect, request, session, url_for
from funciones import obtener_usuario_por_matricula, ver_documento_alumno_uta
import database as dbase
db = dbase.dbConnection()
from bson import ObjectId
from flask import send_file


def init_view(app):
    # Ruta para mostrar el PDF en una nueva ventana o modal
    @app.route('/EduLink/Alumno/ver/<nombre_archivo>/<id_alumno>', methods=['GET'])
    def ver_archivo_alumno_uta(nombre_archivo, id_alumno):
        alumno = obtener_usuario_por_matricula(id_alumno)
        if alumno:
            datos = ver_documento_alumno_uta(id_alumno, nombre_archivo)
            if datos:
                documento_stream = io.BytesIO(datos) 
                documento_stream.seek(0)
                mimetype = 'application/pdf'
                return send_file(documento_stream, as_attachment=False, mimetype=mimetype)
        return 'Archivo no encontrado', 404
    
    @app.route('/EduLink/Alumno/ver/formato_tres_opciones/<id_alumno>', methods=['GET'])
    def ver_archivo_alumno_uta_1(id_alumno):
        

        try:
            id_alumno = ObjectId(id_alumno)
        except Exception as e:
            return 'ID de alumno inválido', 400

        # Busca el documento del alumno
        alumno_documento = db['usuarios'].find_one({'_id': id_alumno})
        

        if alumno_documento and 'formato_tres_opciones' in alumno_documento:
            formato_tres_opciones = alumno_documento['formato_tres_opciones']
            

            if formato_tres_opciones and 'archivo' in formato_tres_opciones:
                archivo = formato_tres_opciones['archivo']
                

                if archivo:
                    datos = archivo
                    documento_stream = io.BytesIO(datos)
                    documento_stream.seek(0)
                    mimetype = 'application/pdf'
                    return send_file(documento_stream, as_attachment=False, mimetype=mimetype)

        return 'Archivo no encontrado', 404


    @app.route('/EduLink/Alumno/Archivos_Universidad/ver/<archivo_id>/', methods=['GET'])
    def ver_archivo(archivo_id):
        conexion = db["archivos_vinculacion"]
        archivo = conexion.find_one({'_id': ObjectId(archivo_id)})

        if archivo:
            nombre = archivo['nombre']
            datos = archivo['archivo']
            documento_stream = io.BytesIO(datos)
            documento_stream.seek(0)
            extension = nombre.split('.')[-1].lower()  # Obtener la extensión del archivo
            if extension == 'pdf':
                mimetype = 'application/pdf'
            elif extension in ['doc', 'docx']:
                mimetype = 'application/msword'
            elif extension in ['xls', 'xlsx']:
                mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            else:
                # Para otros tipos de archivos, establecer el tipo MIME como genérico
                mimetype = 'application/octet-stream'
            return send_file(documento_stream, as_attachment=False, mimetype=mimetype)
        else:
            return 'Archivo no encontrado', 404



    @app.route('/Catalago_De_Empresas/descargar/<archivo_id>/', methods=['GET'])
    def descargar_archivo(archivo_id):
        conexion = db["archivos_vinculacion"]
        archivo = conexion.find_one({'_id': ObjectId(archivo_id)})

        if archivo:
            datos = archivo['archivo']
            nombre = archivo['nombre']
            
            # Obtener la extensión del archivo
            extension = nombre.split('.')[-1].lower()
            
            # Determinar el tipo MIME según la extensión del archivo
            if extension == 'pdf':
                mimetype = 'application/pdf'
            elif extension in ['doc', 'docx']:
                mimetype = 'application/msword'
            elif extension in ['xls', 'xlsx']:
                mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            else:
                # Para otros tipos de archivos, establecer el tipo MIME como genérico
                mimetype = 'application/octet-stream'
            
            return send_file(io.BytesIO(datos), as_attachment=True, mimetype=mimetype, download_name=nombre)
        else:
            return 'Archivo no encontrado', 404

