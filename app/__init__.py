from flask import Flask, request, flash
from flask import render_template
from flask import redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SistemaMarcacion.sqlite3'
app.config['SECRET_KEY'] = 'uippc3'

db = SQLAlchemy(app)

def hora():
    return datetime.now()

"""
   Clase en donde se crea la tablas de la base de datos y se declaran las columnas
    """

class Super(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
    cantidad = db.Column(db.Integer)
    listo = db.Column(db.Boolean, default=False)
    entrada = db.Column(db.String)
    salida = db.Column(db.String)





    def __init__(self, content, cantidad, entrada):
        self.content = content
        self.cantidad = cantidad
        self.entrada = entrada
        self.listo = False




db.create_all()


"""Esta es la Ruta Principal donde se muestran las columnas con sus resultados, se muestra atraves del archivo mostrar_todo.html"""
@app.route('/')
def supers_list():
    supers = Super.query.all()
    return render_template('mostrar_todo.html', supers=supers)

"""     Esta ruta agrega los resultados en la db, si no se agregan datos tira error en el flash
    """
@app.route('/super', methods=['POST'])
def add_super():
    content = request.form.get('content')
    cantidad = request.form.get('cantidad')
    entrada = request.form.get('entrada')

    if not request.form['content'] or not request.form['cantidad']:
        flash('Debes llenar todos los campos')
        return redirect('/')
    super = Super(content,cantidad,entrada)
    db.session.add(super)
    db.session.commit()
    flash('Registro guardado con exito!')
    return redirect('/')

@app.route('/delete/<int:super_id>')
def delete_super(super_id):
    super = Super.query.get(super_id)
    if not super:

        return redirect('/')

    db.session.delete(super)
    db.session.commit()
    flash('Se borro con exito!')
    return redirect('/')

@app.route('/listo/<int:super_id>')
def resolver_super(super_id):
    super = Super.query.get(super_id)

    if not super:
        return redirect('/')
    if super.listo:

        super.listo = False
    else:
        super.listo = True
        time = datetime.now().time()
        print("HORA DE SALIDA:")
        flash('Salio con exito')
        print(time)

    db.session.commit()
    return redirect('/')

var = datetime.now()


app.static_folder = 'static'

if __name__ == '__main__':
    db.create_all()
    app.run()
