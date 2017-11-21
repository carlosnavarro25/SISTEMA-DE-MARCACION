from flask import Flask, request, flash
from flask import render_template
from flask import redirect
from flask_sqlalchemy import SQLAlchemy

"""Aplicacion genera una lista de supermercado
"""

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///listasuper.sqlite3'
app.config['SECRET_KEY'] = 'uippc3'

db = SQLAlchemy(app)


"""
   Clase en donde se crea la tablas de la base de datos y se declaran las columnas
    """

class Super(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
    cantidad = db.Column(db.Integer)
    precio = db.Column(db.Float)
    listo = db.Column(db.Boolean, default=False)

    """
              Este es el metodo constructor de la clase.
          Crea un nueva instancia de :class:`Super`
          :param  content: nombre pde producto
          :param  precio: precio de prducto
          :param  catidad: cantidad de productos
          :type   content: str
          :type   precio: float
          :type   catidad: int
          """

    def __init__(self, content,precio, cantidad):
        self.content = content
        self.precio = precio
        self.cantidad = cantidad
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
    precio = request.form.get('precio')
    cantidad = request.form.get('cantidad')
    if not request.form['content'] or not request.form['precio'] or not request.form['cantidad']:
        flash('Debes llenar todos los campos')
        return redirect('/')
    super = Super(content, precio,cantidad)
    db.session.add(super)
    db.session.commit()
    flash('Registro guardado con exito!')
    return redirect('/')

""" Esta función se encarga de borrar los datos de la base de datos
"""
@app.route('/delete/<int:super_id>')
def delete_super(super_id):
    super = Super.query.get(super_id)
    if not super:

        return redirect('/')

    db.session.delete(super)
    db.session.commit()
    flash('Se borro con exito!')
    return redirect('/')


"""Esta función es Booleana en donde por default esta en False(Sin tachar).
"""

@app.route('/listo/<int:super_id>')
def resolver_super(super_id):
    super = Super.query.get(super_id)

    if not super:
        return redirect('/')
    if super.listo:
        super.listo = False
    else:
        super.listo = True

    db.session.commit()
    return redirect('/')

app.static_folder = 'static'

if __name__ == '__main__':
    db.create_all()
    app.run()