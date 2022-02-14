from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

@app.route('/')
def index():
    # mostrar todas las tareas
    lista_tareas = Tarea.query.all()
    # print(lista_tareas)
    return render_template('index.html', lista_tareas=lista_tareas)

@app.route('/agregar', methods=['POST'])
def add():
    # agregar nueva tarea
    titulo = request.form.get('titulo')
    nueva_tarea = Tarea(title=titulo, complete=False)
    db.session.add(nueva_tarea)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/actualizar/<int:id_tarea>')
def actualizar(id_tarea):
    # actualizar tarea
    tarea = Tarea.query.filter_by(id=id_tarea).first()
    tarea.complete = not tarea.complete
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/eliminar/<int:id_tarea>')
def eliminar(id_tarea):
    # eliminar tarea
    tarea = Tarea.query.filter_by(id=id_tarea).first()
    db.session.delete(tarea)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return "About"

if __name__ == '__main__':
    db.create_all()

    # Crear nueva tarea en la db
    # nueva_tarea = Tarea(title='tarea 1', complete=False)
    # db.session.add(nueva_tarea)
    # db.session.commit()

    app.run(debug=True)