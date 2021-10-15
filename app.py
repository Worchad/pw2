from flask import Flask, render_template, request

app = Flask(__name__)

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
        return "Mi correo es: "+password

if __name__ == '__main_':
    app.run(port=5000, debug=True)