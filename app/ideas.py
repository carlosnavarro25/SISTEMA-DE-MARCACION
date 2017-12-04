"""define un column para todos los modelos"""
class TimestampedModel(Model):
    created_at = Column(DateTime, default=datetime.utcnow)

db = SQLAlchemy(model_class=TimestampedModel)

"""funcion seteando el valor"""
def time():
    return datetime.now()

created_at = Column(Date, default=hora)

"""Como string"""
def time():
    hora = datetime.now()
    return str(datetime.now())

created_at = Column(String, default=hora)
