from flask import Flask, render_template, url_for, send_from_directory, redirect, request, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os




app = Flask(__name__)

app.secret_key = "clave_secreta"
app.config['MYSQL_HOST'] = '3.90.215.92'
app.config['MYSQL_USER'] = 'pieroj'
app.config['MYSQL_PASSWORD'] = 'pjsm1512'
app.config['MYSQL_DB'] = 'floreria_db'

mysql = MySQL(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # Aquí puedes manejar los datos enviados por el formulario
        nombre = request.form['nombre']
        correo = request.form['correo']
        phone = request.form['phone']

        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO usuarios (nombre, correo, phone) VALUES (%s, %s, %s)", (nombre, correo, phone))
            mysql.connection.commit()
            flash('Usuario agregado exitosamente', 'success')
        except Exception as e:
            mysql.connection.rollback()
            flash('Error al agregar usuario: ' + str(e), 'danger')
        finally:
            cur.close()
        return redirect(url_for('index'))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
