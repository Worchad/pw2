from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    usua_id = db.Column(db.Integer, primary_key=True, nullable=False)
    usua_correo = db.Column(db.String(50), unique=True, nullable=False)
    usua_password = db.Column(db.String(60), nullable=False)
    
    def __init__(self,usua_correo,usua_password):
        self.usua_correo = usua_correo
        self.usua_password = usua_password