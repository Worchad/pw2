from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def home():
    titulo = 'Bievenido'
    return render_template('login.html',titulo=titulo)

if __name__ == '__main_':
    app.run(port=5000, debug=True)