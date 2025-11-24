from flask import Flask, render_template, request, flash, redirect, url_for
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from datetime import datetime

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', '123456')  # Clave secreta para sesiones

# Configuración de la base de datos
DB_CONFIG = {
    'host': os.getenv('34.229.154.163'),
    'user': os.getenv('aleqc'),
    'password': os.getenv('123456'),
    'database': os.getenv('pruebita')
}

def get_db_connection():
    """
    Crea y retorna una conexión a la base de datos MySQL
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

def init_db():
    """
    Inicializa la base de datos y crea la tabla si no existe
    """
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    full_name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    phone VARCHAR(20),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            connection.commit()
            print("Base de datos inicializada correctamente")
        except Error as e:
            print(f"Error al inicializar la base de datos: {e}")
        finally:
            cursor.close()
            connection.close()

@app.route('/')
def index():
    """
    Página principal con el formulario de contacto
    """
    return render_template('index.html')

@app.route('/add_contact', methods=['POST'])
def add_contact():
    """
    Procesa el formulario y añade un nuevo contacto
    """
    full_name = request.form.get('full_name', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    
    # Validación básica
    if not full_name or not email:
        flash('El nombre completo y el correo electrónico son obligatorios', 'error')
        return redirect(url_for('index'))
    
    connection = get_db_connection()
    if not connection:
        flash('Error de conexión a la base de datos. Por favor, intente más tarde.', 'error')
        return redirect(url_for('index'))
    
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO contacts (full_name, email, phone) 
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (full_name, email, phone if phone else None))
        connection.commit()
        flash('¡Contacto agregado exitosamente!', 'success')
        return redirect(url_for('contacts'))
    except mysql.connector.IntegrityError:
        flash('Este correo electrónico ya está registrado', 'error')
        return redirect(url_for('index'))
    except Error as e:
        flash(f'Error al guardar el contacto: {str(e)}', 'error')
        return redirect(url_for('index'))
    finally:
        cursor.close()
        connection.close()

@app.route('/contacts')
def contacts():
    """
    Muestra la lista de todos los contactos
    """
    connection = get_db_connection()
    if not connection:
        flash('Error de conexión a la base de datos', 'error')
        return render_template('contacts.html', contacts=[])
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, full_name, email, phone, created_at 
            FROM contacts 
            ORDER BY created_at DESC
        """)
        contacts_list = cursor.fetchall()
        return render_template('contacts.html', contacts=contacts_list)
    except Error as e:
        flash(f'Error al obtener los contactos: {str(e)}', 'error')
        return render_template('contacts.html', contacts=[])
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)