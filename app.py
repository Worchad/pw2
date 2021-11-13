from flask import Flask,redirect,url_for,render_template,request,flash,json
from config import ConfiguracionDesarrollo
from model import db, Usuarios
from sqlalchemy.ext.declarative import DeclarativeMeta

app=Flask(__name__)
app.config.from_object(ConfiguracionDesarrollo)
db.init_app(app)

@app.route('/', methods = ['GET', 'POST'])
def home():
    titulo = 'Bievenido'
    return render_template('login.html',titulo=titulo)

@app.route('/procesar_credenciales', methods = ['POST'])
def procesarCredenciales():
    if request.method=='POST':
        datos = request.form
        correo = datos['txtCorreo']
        password = datos['txtPassword']
        if(correo=="" or password==""):
            flash("Debe completar los campos","alerta")
            return redirect(url_for('home'))
        else:
            comprobar = Usuarios.query.filter_by(usua_correo = correo, usua_password = password).first()
            if comprobar is not None:
                flash("Las credenciales ingresadas son correctas", "correcto")
                return redirect(url_for('principal'))
            else:
                flash("Credenciales incorrectas","alerta")
                return redirect(url_for('home'))

@app.route('/principal')
def principal():
    return render_template('index.html')

@app.route('/obtener_usuarios', methods=['POST'])
def obtenerUsuarios():
    if request.method == 'POST':
        datos = request.form
        codigo = datos['cod']
        if codigo == "":
            usuarios = Usuarios.query.all()
        else:
            usuarios = Usuarios.query.filter_by(usua_id = codigo).all()
    
    return json.dumps(usuarios, cls=AlchemyEncoder)


@app.route('/alta_usuarios', methods=['POST'])
def altaUsuarios():
    mensajes = ""
    if request.method == 'POST':
        datos = request.form
        correo = datos['txtCorreo']
        password = datos['txtPassword']
        if(correo=="" or password==""):
            mensajes = 'Debe completar los campos'
        else:
            registro = Usuarios(usua_correo=correo, usua_password=password)
            db.session.add(registro)
            db.session.commit()
            mensajes = 'Usuario ha sido registrado correctamente'
    return json.dumps(mensajes)

@app.route('/modificacion_usuarios', methods=['POST'])
def modificacionUsuarios():
    mensajes = ""
    if request.method == 'POST':
        datos = request.form
        codigo = datos['txtCodigo']
        correo = datos['txtCorreo']
        password = datos['txtPassword']
        if(correo == "" or password == "" or codigo == ""):
            mensajes = 'Debe completar los campos y/o seleccionar al usuario'
        else:
            modificacion = Usuarios.query.filter_by(usua_id=codigo).first()
            modificacion.usua_correo = correo
            modificacion.usua_password = password
            db.session.commit()
            mensajes = 'Usuario ha sido modificado correctamente'
    return json.dumps(mensajes)

@app.route('/baja_usuarios', methods=['POST'])  
def bajaUsuarios():
    mensajes = ""
    if request.method == 'POST':
        datos = request.form
        codigo = datos['cod']
        if(codigo == ""):
            mensajes = 'Debe seleccionar al usuario'
        else:
            eliminar = Usuarios.query.filter_by(usua_id=codigo).first()
            db.session.delete(eliminar)
            db.session.commit()
            mensajes = 'Usuario ha sido eliminado correctamente'
    return json.dumps(mensajes)

class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            return fields
        return json.JSONEncoder.default(self,obj)

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)
