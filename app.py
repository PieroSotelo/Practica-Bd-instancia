from flask import Flask, render_template, url_for, send_from_directory, redirect, request, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os




app = Flask(__name__)

app.secret_key = "clave_secreta"
app.config['MYSQL_HOST'] = '54.83.118.199'
app.config['MYSQL_USER'] = 'pieroj'
app.config['MYSQL_PASSWORD'] = 'pjsm1512'
app.config['MYSQL_DB'] = 'floreria_db'

mysql = MySQL(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        correo = request.form.get('correo', '').strip()
        phone = request.form.get('phone', '').strip()

        if not nombre or not correo or not phone:
            flash('Todos los campos son requeridos', 'danger')
            return redirect(url_for('index'))

        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO usuarios (nombre, correo, phone) VALUES (%s, %s, %s)", (nombre, correo, phone))
            mysql.connection.commit()
            flash('Usuario agregado exitosamente', 'success')
        except Exception as e:
            mysql.connection.rollback()
            flash('Error al agregar usuario: ' + str(e), 'danger')
            return redirect(url_for('index'))
        finally:
            cur.close()
        return redirect(url_for('contacts'))
    return render_template('index.html')

@app.route('/contacts', methods=['GET'])
def contacts():
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT id, nombre, correo, phone FROM usuarios")
        usuarios = cur.fetchall()
    except Exception as e:
        usuarios = []
        flash('Error al obtener usuarios: ' + str(e), 'danger')
    finally:
        cur.close()
    return render_template('contacts.html', usuarios=usuarios)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
