from flask import Flask, send_file, request, render_template, redirect, jsonify
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
import os
import datetime
import secrets
import sqlite3

url = "http://tareasyrefuerzos.tk/"
email_id = 'tareasyrefuerzosco@gmail.com'
pass_id = ""
email_admin = 'tareas_refuerzos@hotmail.com'
mainlogo = url+"images/icon.png"
urlfiles = url+"archivos/"
FILE_PATH = '/var/www/html/TareasyRefuerzos/files/'

app = Flask(__name__)

app.config['UPLOAD_EXTENSIONS'] = ['.rar','.pdf','.jpg','.jpeg','.gif','.png','.doc','.docx','.xls','.xlsx','.txt']
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = email_id
app.config['MAIL_PASSWORD'] = pass_id
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['UPLOAD_FOLDER'] = FILE_PATH
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////var/www/html/TareasyRefuerzos/database/database.db'

db = SQLAlchemy(app)
mail = Mail(app)

def fecha_hora(fecha,hora):
    formato_fecha = "%A %d de %B"
    formato_hora = "%I:%M %p"
    try:
        fecha = datetime.datetime.strptime(fecha, "%Y-%m-%d")
        fecha = str(fecha.strftime(formato_fecha))
    except:
        pass
    try:
        hora = datetime.datetime.strptime(hora, "%H:%M")
        hora = str(hora.strftime(formato_hora))
    except:
        pass
    return fecha+" "+hora

class Trabajos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idkey = db.Column(db.String(255))
    nombre = db.Column(db.String(255))
    carrera = db.Column(db.String(255))
    materia = db.Column(db.String(255))
    tema = db.Column(db.String(255))
    correo = db.Column(db.String(255))
    celular = db.Column(db.String(255))
    fecha = db.Column(db.String(255))
    hora = db.Column(db.String(255))
    medio = db.Column(db.String(255))
    detalles = db.Column(db.Text)
    adjuntos = db.Column(db.Text)

class Examenes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idkey = db.Column(db.String(255))
    nombre = db.Column(db.String(255))
    carrera = db.Column(db.String(255))
    materia = db.Column(db.String(255))
    tema = db.Column(db.String(255))
    tiempo = db.Column(db.String(255))
    formato = db.Column(db.String(255))
    correo = db.Column(db.String(255))
    celular = db.Column(db.String(255))
    fecha = db.Column(db.String(255))
    hora = db.Column(db.String(255))
    medio = db.Column(db.String(255))
    detalles = db.Column(db.Text)
    adjuntos = db.Column(db.Text)

class Clases(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idkey = db.Column(db.String(255))
    nombre = db.Column(db.String(255))
    carrera = db.Column(db.String(255))
    materia = db.Column(db.String(255))
    tema = db.Column(db.String(255))
    tiempo = db.Column(db.String(255))
    formato = db.Column(db.String(255))
    correo = db.Column(db.String(255))
    celular = db.Column(db.String(255))
    fecha = db.Column(db.String(255))
    hora = db.Column(db.String(255))
    medio = db.Column(db.String(255))
    detalles = db.Column(db.Text)
    adjuntos = db.Column(db.Text)
    

@app.route("/")
def index():
    return render_template("index.html"),200

@app.route("/sw.js")
def sw():
    return app.send_static_file("sw.js"),200

@app.route("/telefonos/<telefono>")
def telefonos(telefono):
    return redirect('https://api.whatsapp.com/send?phone=57'+telefono)

@app.route("/trabajos")
def trabajos():
    return render_template("trabajos.html"),200

@app.route("/examenes")
def examenes():
    return render_template("examenes.html"),200

@app.route("/clases")
def clases():
    return render_template("clases.html"),200

@app.route("/images/<string:imagen>")
def image(imagen):
    return send_file("static/"+imagen),200

@app.route("/archivos/<string:archivo>")
def archivos(archivo):
    return send_file(FILE_PATH+archivo),200

@app.route("/borrar", methods=['POST','GET'])
def borrar():
    if request.method == 'POST':
        files = request.form.getlist('file')[0]
        try:
            os.remove(FILE_PATH+files)
        except:
            pass
    return "OK",200

@app.route("/file", methods=['POST','GET'])
def file():
    if request.method == 'POST':
        files = request.files.getlist('file')
        data = []
        for file in files:
            filename = file.filename
            ext = os.path.splitext(filename)[1]
            name = "TYR"+datetime.date.today().strftime("%Y%m%d")+secrets.token_urlsafe(16)+ext
            if ext in app.config['UPLOAD_EXTENSIONS']:
                file.save(app.config['UPLOAD_FOLDER']+name)
            data.append({'name':filename,'file':name})
    return jsonify(data),200

@app.route("/subtrabajos", methods=['POST','GET'])
def subtrabajos():
    if request.method == "POST":
        nombre = request.form.getlist('nombre')[0]
        carrera = request.form.getlist('carrera')[0]
        materia = request.form.getlist('materia')[0]
        tema = request.form.getlist('tema')[0]
        correo = request.form.getlist('correo')[0]
        celular = request.form.getlist('celular')[0]
        fecha = request.form.getlist('fecha')[0]
        hora = request.form.getlist('hora')[0]
        medio = request.form.getlist('medio')[0]
        detalles = request.form.getlist('detalles')[0]
        files = request.form.getlist('subfile')[0]
        entrega = fecha_hora(fecha,hora)
        if medio == 'celular':
            medio = 'WhatsApp'
        else:
            medio = 'Correo'
        adjuntos = ""
        files = files.split(",")
        if files[0]!='':
            for i in files:
                adjuntos = adjuntos+urlfiles+i+", "
        idkey = "TYR"+datetime.date.today().strftime("%Y%m%d")+secrets.token_urlsafe(8)
        trabajos = Trabajos(idkey=idkey,
                            nombre=nombre,
                            carrera=carrera,
                            materia=materia,
                            tema=tema,
                            correo=correo,
                            celular=celular,
                            fecha=fecha,
                            hora=hora,
                            medio=medio,
                            detalles=detalles,
                            adjuntos=adjuntos)
        db.session.add(trabajos)
        db.session.commit()
        msg = Message('Cotización nueva',
                      sender=email_id,
                      recipients = [email_admin])
        msg.html = render_template('trabajos_admin.html',
                                   logo=mainlogo,
                                   nombre=nombre,
                                   carrera=carrera,
                                   materia=materia,
                                   tema=tema,
                                   correo=correo,
                                   celular=celular,
                                   telefono='https://api.whatsapp.com/send?phone=57'+celular,
                                   entrega=entrega,
                                   medio=medio,
                                   detalles=detalles,
                                   archivos=adjuntos)
        mail.send(msg)
        msg = Message('Cotización nueva',
                      sender=email_id,
                      recipients = [email_admin])
        msg.html = render_template('trabajos_asesor.html',
                                   logo=mainlogo,
                                   materia=materia,
                                   tema=tema,
                                   entrega=entrega,
                                   detalles=detalles,
                                   archivos=adjuntos)
        mail.send(msg)
    return render_template("confirmacion.html"),200

@app.route("/subexamenes", methods=['POST','GET'])
def subexamenes():
    if request.method == "POST":
        nombre = request.form.getlist('nombre')[0]
        materia = request.form.getlist('materia')[0]
        carrera = request.form.getlist('carrera')[0]
        tema = request.form.getlist('tema')[0]
        tiempo = request.form.getlist('tiempo')[0]
        formato = request.form.getlist('formato')[0]
        correo = request.form.getlist('correo')[0]
        celular = request.form.getlist('celular')[0]
        fecha = request.form.getlist('fecha')[0]
        hora = request.form.getlist('hora')[0]
        medio = request.form.getlist('medio')[0]
        detalles = request.form.getlist('detalles')[0]
        files = request.form.getlist('subfile')[0]
        entrega = fecha_hora(fecha,hora)  
        if medio == 'celular':
            medio = 'WhatsApp'
        else:
            medio = 'Correo'
        adjuntos = ""
        files = files.split(",")
        if files[0]!='':
            for i in files:
                adjuntos = adjuntos+urlfiles+i+", "
        idkey = "TYR"+datetime.date.today().strftime("%Y%m%d")+secrets.token_urlsafe(8)
        examenes = Examenes(idkey=idkey,
                            nombre=nombre,
                            carrera=carrera,
                            materia=materia,
                            tema=tema,
                            tiempo=tiempo,
                            formato=formato,
                            correo=correo,
                            celular=celular,
                            fecha=fecha,
                            hora=hora,
                            medio=medio,
                            detalles=detalles,
                            adjuntos=adjuntos)
        db.session.add(examenes)
        db.session.commit()
        msg = Message('Cotización nueva',
                      sender=email_id,
                      recipients = [email_admin])
        msg.html = render_template('examenes_admin.html',
                                   logo=mainlogo,
                                   nombre=nombre,
                                   carrera=carrera,
                                   materia=materia,
                                   tema=tema,
                                   tiempo=tiempo,
                                   formato=formato,
                                   correo=correo,
                                   celular=celular,
                                   telefono='https://api.whatsapp.com/send?phone=57'+celular,
                                   entrega=entrega,
                                   medio=medio,
                                   detalles=detalles,
                                   archivos=adjuntos)
        mail.send(msg)
        msg = Message('Cotización nueva',
                      sender=email_id,
                      recipients = [email_admin])
        msg.html = render_template('examenes_asesor.html',
                                   logo=mainlogo,
                                   materia=materia,
                                   tema=tema,
                                   tiempo=tiempo,
                                   formato=formato,
                                   entrega=entrega,
                                   detalles=detalles,
                                   archivos=adjuntos)
        mail.send(msg)
    return render_template("confirmacion.html"),200

@app.route("/subclases", methods=['POST','GET'])
def subclases():
    if request.method == "POST":
        nombre = request.form.getlist('nombre')[0]
        materia = request.form.getlist('materia')[0]
        carrera = request.form.getlist('carrera')[0]
        tema = request.form.getlist('tema')[0]
        tiempo = request.form.getlist('tiempo')[0]
        formato = request.form.getlist('formato')[0]
        correo = request.form.getlist('correo')[0]
        celular = request.form.getlist('celular')[0]
        fecha = request.form.getlist('fecha')[0]
        hora = request.form.getlist('hora')[0]
        medio = request.form.getlist('medio')[0]
        detalles = request.form.getlist('detalles')[0]
        files = request.form.getlist('subfile')[0]
        entrega = fecha_hora(fecha,hora)
        if medio == 'celular':
            medio = 'WhatsApp'
        else:
            medio = 'Correo'
        adjuntos = ""
        files = files.split(",")
        if files[0]!='':
            for i in files:
                adjuntos = adjuntos+urlfiles+i+", "
        idkey = "TYR"+datetime.date.today().strftime("%Y%m%d")+secrets.token_urlsafe(8)
        clases = Clases(idkey=idkey,
                        nombre=nombre,
                        carrera=carrera,
                        materia=materia,
                        tema=tema,
                        tiempo=tiempo,
                        formato=formato,
                        correo=correo,
                        celular=celular,
                        fecha=fecha,
                        hora=hora,
                        medio=medio,
                        detalles=detalles,
                        adjuntos=adjuntos)
        db.session.add(clases)
        db.session.commit()
        msg = Message('Cotización nueva',
                      sender=email_id,
                      recipients = [email_admin])
        msg.html = render_template('clases_admin.html',
                                   logo=mainlogo,
                                   nombre=nombre,
                                   carrera=carrera,
                                   materia=materia,
                                   tema=tema,
                                   tiempo=tiempo,
                                   formato=formato,
                                   correo=correo,
                                   celular=celular,
                                   telefono='https://api.whatsapp.com/send?phone=57'+celular,
                                   entrega=entrega,
                                   medio=medio,
                                   detalles=detalles,
                                   archivos=adjuntos)
        mail.send(msg)
        msg = Message('Cotización nueva',
                      sender=email_id,
                      recipients = [email_admin])
        msg.html = render_template('clases_asesor.html',
                                   logo=mainlogo,
                                   materia=materia,
                                   tema=tema,
                                   tiempo=tiempo,
                                   formato=formato,
                                   entrega=entrega,
                                   detalles=detalles,
                                   archivos=adjuntos)
        mail.send(msg)
    return render_template("confirmacion.html"),200

if __name__ == "__main__":
    app.run(debug = True, port = 80, host = '0.0.0.0')
