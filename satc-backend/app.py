from quart import Quart, jsonify, render_template, request
from opcua_client import connect_to_sam, disconnect_from_sam, read_data_from_sam
import asyncpg
from db_connect import db_config
from quart_cors import cors

app = Quart(__name__)
app = cors(app, allow_origin="*")

@app.route('/')
async def hello():
    return '¡Hola desde el backend del proyecto SATC!'

@app.route('/read_data')
async def read_data():
    sam_url = "opc.tcp://opcua_server:4840"  # URL del servidor OPC UA del SAM
    sam_client = await connect_to_sam(sam_url)
    if sam_client:
        object_node_id = "ns=2;i=1"  # Reemplaza esto con el NodeId del objeto que contiene las variables
        sensor_data_list = await read_data_from_sam(sam_client, object_node_id)
        await disconnect_from_sam(sam_client)
        if sensor_data_list:
            print(f"Datos recibidos del endpoint /read_data: {sensor_data_list}")  # Impresión de depuración
            return jsonify({"data": sensor_data_list})
        else:
            print("No se recibieron datos del SAM")  # Impresión de depuración
            return jsonify({"error": "No se recibieron datos del SAM"})
    else:
        print("No se pudo conectar al SAM")  # Impresión de depuración
        return jsonify({"error": "No se pudo conectar al SAM"})


@app.route('/api/register_machines', methods=['POST'])
async def add_machine():
    data = await request.get_json()  # Retrieve JSON data from the request
    conn = await asyncpg.connect(**db_config)  # Connect to the PostgreSQL database

    # Insertar la nueva máquina y obtener su ID
    machine_query = '''INSERT INTO maquina(nombre, ubicacion, descripcion)
                       VALUES($1, $2, $3) RETURNING id;'''
    machine_values = (data['nombre'], data['ubicacion'], data['descripcion'])
    new_machine_id = await conn.fetchval(machine_query, *machine_values)

    # Insertar los sensores asociados con la nueva máquina
    for sensor in data['sensores']:
        sensor_query = '''INSERT INTO sensor(nombre, tipo, unidad_medida, maquina_id)
                          VALUES($1, $2, $3, $4);'''
        await conn.execute(sensor_query, sensor['nombre'], sensor['tipo'], sensor['unidad_medida'], new_machine_id)

    await conn.close()  # Close the database connection
    return jsonify({"new_machine_id": new_machine_id}), 201  # Return the inserted row's ID as JSON response

@app.route('/maquinas')
async def show_machines():
    return await render_template('maquinas.html')

@app.route('/api/get_machines')
async def get_machines():
    conn = await asyncpg.connect(**db_config)
    machines = await conn.fetch('SELECT * FROM maquina;')
    machines_data = []
    for machine in machines:
        sensors = await conn.fetch('SELECT * FROM sensor WHERE maquina_id = $1;', machine['id'])
        machines_data.append({
            'id': machine['id'],
            'nombre': machine['nombre'],
            'ubicacion': machine['ubicacion'],
            'descripcion': machine['descripcion'],
            'sensores': sensors
        })
    await conn.close()
    return jsonify(machines_data)
                      
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)