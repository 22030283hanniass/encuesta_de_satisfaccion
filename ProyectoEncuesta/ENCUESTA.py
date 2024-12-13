import mysql.connector 
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# Conexión a MySQL
def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="hanniaadmin",
        database="encuesta_de_satisfaccion"
    )
    return connection

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/seleccionar_tipo', methods=['POST'])
def seleccionar_tipo():
    tipo_usuario = request.form['tipo_usuario']
    
    if tipo_usuario == 'empleado':
        return redirect(url_for('empleado'))
    elif tipo_usuario == 'alumno':
        return redirect(url_for('alumno'))

@app.route('/alumno')
def alumno():
    # Carreras cargadas de forma estática
    carreras = [
        "Ingeniería en Datos",
        "Ingeniería en Robótica",
        "Ingeniería en Energía"
    ]
    
    # Los departamentos sí se obtienen de la base de datos
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT departamento FROM empleados ORDER BY departamento ASC")
    departamentos = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('seleccionar_departamento_alumno.html', carreras=carreras, departamentos=departamentos)


@app.route('/empleado')
def empleado():
    # Obtener los departamentos desde la base de datos
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT departamento FROM empleados ORDER BY departamento ASC")
    departamentos = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('seleccionar_departamento_empleado.html', departamentos=departamentos)

@app.route('/empleados/<departamento>', methods=['GET'])
def cargar_empleados(departamento):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT CONCAT(nombre, ' ', apellido_paterno, ' ', apellido_materno) AS nombre_completo
            FROM empleados
            WHERE LOWER(departamento) = LOWER(%s)
            ORDER BY nombre_completo ASC
        """, (departamento.strip(),))
        empleados = [row[0] for row in cursor.fetchall()]
        if not empleados:
            return jsonify([])  # Retorna lista vacía si no hay empleados
    except mysql.connector.Error as err:
        print(f"Error al cargar empleados: {err}")
        return jsonify({"error": "Error al cargar empleados desde la base de datos"}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify(empleados)

@app.route('/encuesta_empleado', methods=['POST'])
def encuesta_empleado():
    departamento = request.form['departamento']
    empleado = request.form['empleado']
    
    # Lógica para la encuesta del empleado
    return render_template('encuesta.html', departamento=departamento, empleado=empleado)

@app.route('/encuesta_alumno', methods=['POST'])
def encuesta_alumno():
    # Recoge los datos del formulario inicial
    carrera = request.form['carrera']
    departamento = request.form['departamento']
    
    # Renderiza la página de la encuesta con los datos recibidos
    return render_template('encuesta.html', carrera=carrera, departamento=departamento)

@app.route('/procesar_encuesta', methods=['POST'])
def procesar_encuesta():
    # Recoge las respuestas de la encuesta
    respuestas = request.form.to_dict()  # Todas las respuestas del formulario
    print(f"Respuestas recibidas: {respuestas}")  # Opcional: para depuración

    # Redirige a la página de agradecimiento
    return redirect(url_for('gracias'))

@app.route('/guardar_respuestas', methods=['POST'])
def guardar_respuestas():
    # Guardar las respuestas de la encuesta en la base de datos
    respuestas = request.form.to_dict()
    connection = get_db_connection()
    cursor = connection.cursor()

    for pregunta, respuesta in respuestas.items():
        cursor.execute("INSERT INTO respuestas (pregunta, respuesta) VALUES (%s, %s)", (pregunta, respuesta))

    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for('gracias'))

@app.route('/preguntas', methods=['POST'])
def preguntas():
    # Lógica para mostrar las preguntas de la encuesta
    return render_template('encuesta.html')

@app.route('/gracias')
def gracias():
    print("Ruta /gracias fue llamada")
    return render_template('gracias.html')

if __name__ == '__main__':
    app.run(debug=True)