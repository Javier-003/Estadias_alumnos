
import bcrypt
from bson import ObjectId
from flask import flash, redirect, render_template, request, session, url_for
from funciones import nocache
import database as dbase
db = dbase.dbConnection()
def init_create(app):


    @app.route("/Registrarse/", methods=['POST'])
    def Registrarse():
        alumnos = db["usuarios"]
        if request.method == 'POST':
            correo = request.form['correoAlumn']
            matricula = request.form['matricula_Alum']
            existing_alumno = alumnos.find_one({
                '$or': [
                    {'correoAlumno': correo},
                    {'matricula': matricula}
                ]
            })
            if existing_alumno:
                flash ('El correo o la matrícula ya están registrados.','warning')
                return redirect(url_for('administrarAlumno'))

            nombre = request.form['Nombre_Alumn']
            apellidos = request.form['apellidos_Alum']
            carrera = request.form['idCarrera']
            estadia = request.form['estadia']
            periodo = request.form['idPeriodo']
            grupo = request.form['grupo']
            telefono =request.form['telefonoAlumno']
            password = request.form['contraseñaAlumn']
            hashpass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            alumnos.insert_one({
                'nombreAlumno': nombre,
                'telefonoAlumno':telefono,
                'apellidosAlumno': apellidos,
                'grupo': grupo ,
                'matricula': matricula,
                'correoAlumno': correo,
                'contraseñaAlumno': hashpass,
                'idCarrera': carrera,
                'estadiaAlumno': estadia,
                'idPeriodo': periodo,
                "tipo_estadia":'no asignado',
                "estatus_servicios": 'no asignado',
                "estatus_finanzas": 'no asignado',
                "folio_finanzas":'no asignado',
                "seguimiento_estadia":'no asignado',
                "formato_tres_opciones": {"estado": "activo", "archivo": None, "comentario": None}
            })
            flash ('Alumno registrado exitosamente.','success')
            return redirect(url_for('login'))
        else:
            flash ('El alumno no se pudo registrar.','danger')
        return redirect(url_for('registro'))

    

   
        if request.method == 'POST':
            conexion = db['carreras']
            nombreCarrera = request.form['N_carrera']
            abreviatura = request.form['Abreviatura']


            carrera_existente = conexion.find_one({'NombreCarrera': nombreCarrera})

            if carrera_existente is None:
                conexion.insert_one({
                    'NombreCarrera': nombreCarrera,
                    'Abreviatura': abreviatura,
                })
                flash('Carrera agregada correctamente', 'success')
                return redirect(url_for('Carrera'))
            
            flash('Carrera ya existente', 'danger')
        return redirect(url_for('Carrera'))

