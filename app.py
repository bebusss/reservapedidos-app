from flask import Flask, render_template, request, jsonify
import requests  # Usaremos requests para enviar el mensaje a Telegram
from connection import obtener_conexion  

app = Flask(__name__)

TELEGRAM_TOKEN = '7693678178:AAHyiQXXQJRz-Dbe240xTY-62G_fSvMf8uc'  # Sustituye con tu token de bot
CHAT_ID = '5058725201'  # Sustituye con tu chat ID

def enviar_mensaje_telegram(mensaje):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    params = {
        'chat_id': CHAT_ID,
        'text': mensaje
    }
    response = requests.post(url, params=params)
    if response.status_code != 200:
        print(f"Error al enviar mensaje: {response.text}")  # Log de error en el envío
    else:
        print("Mensaje enviado correctamente")  # Confirmación de mensaje enviado

@app.route('/pedidos', methods=['GET', 'POST'])
def pedidos():
    if request.method == 'GET':
        return render_template('pedidos.html')

    if request.method == 'POST':
        data = request.form
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Verificar si el UsuarioID existe en la tabla Usuarios
        query_check_usuario = "SELECT COUNT(*) FROM Usuarios WHERE UsuarioID = ?"
        cursor.execute(query_check_usuario, (data['UsuarioID'],))
        usuario_exists = cursor.fetchone()[0]

        if usuario_exists == 0:
            return jsonify({'error': 'El UsuarioID proporcionado no existe en la base de datos'}), 400

        try:
            # Insertar el pedido en la base de datos
            query = """
                INSERT INTO Pedidos (UsuarioID, Estado, Total)
                VALUES (?, 'En preparación', ?);
            """
            cursor.execute(query, (data['UsuarioID'], data['Total']))
            conexion.commit()

            # Enviar mensaje de Telegram para el pedido
            mensaje_telegram = f"Nuevo pedido registrado:\nUsuarioID: {data['UsuarioID']}\nTotal: {data['Total']}"
            enviar_mensaje_telegram(mensaje_telegram)

        except Exception as e:
            conexion.rollback()  # Revertir cambios en caso de error
            return jsonify({'error': str(e)}), 500
        finally:
            conexion.close()

        return jsonify({'message': 'Pedido registrado con éxito'}), 201

@app.route('/reservas', methods=['GET', 'POST'])
def reservas():
    if request.method == 'GET':
        return render_template('reservas.html')

    if request.method == 'POST':
        data = request.form
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Verificar si el UsuarioID existe en la tabla Usuarios
        query_check_usuario = "SELECT COUNT(*) FROM Usuarios WHERE UsuarioID = ?"
        cursor.execute(query_check_usuario, (data['UsuarioID'],))
        usuario_exists = cursor.fetchone()[0]

        if usuario_exists == 0:
            return jsonify({'error': 'El UsuarioID proporcionado no existe en la base de datos'}), 400

        try:
            # Insertar la reserva en la base de datos
            query = """
                INSERT INTO Reservas (UsuarioID, FechaReserva, HoraReserva, NumeroPersonas, Estado)
                VALUES (?, ?, ?, ?, 'Pendiente');
            """
            cursor.execute(query, (data['UsuarioID'], data['FechaReserva'], data['HoraReserva'], data['NumeroPersonas']))
            conexion.commit()

            # Enviar mensaje de Telegram para la reserva
            mensaje_telegram = f"Nueva reserva registrada:\nUsuarioID: {data['UsuarioID']}\nFecha: {data['FechaReserva']}\nHora: {data['HoraReserva']}\nNúmero de personas: {data['NumeroPersonas']}"
            enviar_mensaje_telegram(mensaje_telegram)

        except Exception as e:
            conexion.rollback()  # Revertir cambios en caso de error
            return jsonify({'error': str(e)}), 500
        finally:
            conexion.close()

        return jsonify({'message': 'Reserva registrada con éxito'}), 201

if __name__ == '__main__':
    app.run(debug=True)
