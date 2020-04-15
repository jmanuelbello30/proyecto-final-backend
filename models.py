from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    user_type = db.Column(db.String(100), nullable=False) 
    #Relación one-to-one con los modelos Paciente y Profesional, por lo tanto 
    #parámetro debe ser uselist=False
    #professional = db.relationship('Professional', uselist=False, backref='professional', lazy=True)
    #patient = db.relationship('Patient', uselist=False, backref='patient', lazy=True)   

    def __repr__(self):
        return '<User &r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "user_type": self.user_type,
            #"professional": self.professional_id,
            #"patient": self.patient_id
       }

psicological_therapy = db.Table('psicological_therapy',
    db.Column('professional_id', db.Integer, db.ForeignKey('professionals.id'), primary_key=True),
    db.Column('patient_id', db.Integer, db.ForeignKey('patients.id'), primary_key=True)
)

class Professional(db.Model):
    __tablename__='professionals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rut = db.Column(db.String(100), nullable=True, default="sin-foto.png")
    certification = db.Column(db.String(100), nullable=False, default="sin-foto.png")
    numberid = db.Column(db.String(100), nullable=False, default="sin-foto.png")
    curriculum = db.Column(db.String(100), nullable=False, default="sin-foto.png")
    # Todos los documentos son obligatorios para procesar el registro
    #user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    #patients = db.relationship('Patient', secondary=psicological_therapy, lazy='subquery',
    #backref=db.backref('professionals', lazy=True))    
    #status = db.relationship('Professional_Status', uselist=False, backref='professional', lazy=True)
    #mesagges = db.relationship('Message_Sent', backref='professional', lazy=True)

    def __repr__(self):
        return "<Professional %r>" % self.name
    
    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "rut": self.rut
            #"email": self.user.email
            #"perfil": self.perfil.serialize()
        }

class Status_Professional(db.Model):
    __tablename__='status_professionals'
    id = db.Column(db.Integer, primary_key=True)
    available = db.Column(db.String(120), nullable=False)
    #professional_id = db.Column(db.Integer, db.ForeignKey('professionals.id'),
    #   nullable=False)
    panic_alerts_id = db.Column(db.Integer, db.ForeignKey('alerts.id'),
        nullable=False)
    
    def __repr__(self):
        return "<Status_Professional %r>" % self.available
    
    def serialize(self):
        return{
            "id": self.id,
            "available": self.available,
            #"professional_id": self.professional_id,
            "panic_alerts_id": self.panic_alerts_id,
        }
    

class Patient(db.Model):
    __tablename__='patients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    alerts = db.relationship('Panic_Alert', backref='patient', lazy=True)
    mesagges_sent = db.relationship('Message_Sent', backref='Professional', lazy=True)
    #user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    def __repr__(self):
        return '<Patient &r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "alerts": self.alerts,
            "message_sent": self.mesagges_sent
        }

class Panic_Alert(db.Model):
    __tablename__='alerts'
    id = db.Column(db.Integer, primary_key=True)
    alert = db.Column(db.String(120), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'),
        nullable=False)
    status = db.relationship('Status_Professional', backref='alerts', lazy=True)

    def __repr__(self):
        return '<Panic_Alert &r>' % self.alert

    def serialize(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "alert": self.alert,
            "status": self.status
        }

class Message_Sent(db.Model):
    __tablename__='messages'
    id = db.Column(db.Integer, primary_key=True)
    msg_sent = db.Column(db.String(120), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    professional_id = db.Column(db.Integer, db.ForeignKey('professionals.id'),
        nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'),
        nullable=False)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'),
        nullable=False)
    
    def __repr__(self):
        return '<Message_Sent &r>' % self.msg_sent

    def serialize(self):
        return {
            "id": self.id,
            "msg_sent": self.msg_sent,
            "timestamp": self.timestamp,
            "message_sent": self.mesagges_sent,
            "professional_id": self.professional_id,
            "patient_id": self.patient_id
        }

class Chat_Room(db.Model):
    __tablename__='chat'
    id = db.Column(db.Integer, primary_key=True)
    chat_history = db.Column(db.String(50), nullable=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # mesagges_sent = db.relationship('Message_Sent', backref='Professional', lazy=True)

    def __repr__(self):
        return "<Chat_Room %r>" % self.id
    
    def serialize(self):
        return{
            "id": self.id,
            "chat_history": self.chat_history,
            "timestamp": self.timestamp,
            "mesagges_sent": self.mesagges_sent
        }