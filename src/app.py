from flask import Flask, flash, render_template, redirect, url_for, request, session
from dao.DAOUsuario import DAOUsuario


app = Flask(__name__)
app.secret_key = "Ut3c_123456" #texto super largo 

db = DAOUsuario()



@app.route('/')   #root route
def inicio():
#    return "UTEC - rosario quispe"
    return render_template('index.html')




@app.route('/usuario/')  
def index():
    datos = db.read(None)
    return render_template('usuario/index.html', data=datos)


@app.route('/usuario/add/')
def add():
    return render_template('/usuario/add.html')

@app.route('/usuario/addusuario', methods = ['POST', 'GET'])
def addusuario():
    if request.method == 'POST' and request.form['save']:
        if db.insert(request.form):
            flash("Nuevo usuario creado")
        else:
            flash("ERROR, al crear usuario")

        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/usuario/update/<int:id>/')
def update(id):
    data = db.read(id);

    if len(data) == 0:
        return redirect(url_for('index'))
    else:
        session['update'] = id
        return render_template('usuario/update.html', data = data)

@app.route('/usuario/updateusuario', methods = ['POST'])
def updateusuario():
    if request.method == 'POST' and request.form['update']:

        if db.update(session['update'], request.form):
            flash('Se actualizo correctamente')
        else:
            flash('ERROR en actualizar')

        session.pop('update', None)

        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/usuario/delete/<int:id>/')
def delete(id):
    data = db.read(id);

    if len(data) == 0:
        return redirect(url_for('index'))
    else:
        session['delete'] = id
        return render_template('usuario/delete.html', data = data)

@app.route('/usuario/deleteusuario', methods = ['POST'])
def deleteusuario():
    if request.method == 'POST' and request.form['delete']:

        if db.delete(session['delete']):
            flash('Usuario eliminado')
        else:
            flash('ERROR al eliminar')
        session.pop('delete', None)

        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


# ----------------------------------------------------------------
@app.route('/login')
def loginPage():
    return render_template('login.html', title='Login Page')
 
@app.route('/about')
def aboutPage():
    return render_template('about.html', title='About')

if __name__ == '__main__':
    app.run(port=5000, host="0.0.0.0",debug=True)  #port 5000 por defecto 

