from quart import Quart, jsonify, request
from opcua_client import connect_to_sam, disconnect_from_sam, read_data_from_sam
import asyncpg
from db_connect import db_config

app = Quart(__name__)

@app.route('/')
async def hello():
    return '¡Hola desde el backend del proyecto SATC!'

@app.route('/read_data')
async def read_data():
    sam_url = "opc.tcp://opcua_server:4840"  # URL del servidor OPC UA del SAM
    sam_client = await connect_to_sam(sam_url)
    if sam_client:
        object_node_id = "ns=2;i=1"  # Reemplaza esto con el NodeId del objeto que contiene las variables
        data = await read_data_from_sam(sam_client, object_node_id)
        await disconnect_from_sam(sam_client)
        print(f"Datos recibidos del endpoint /read_data: {data}")  # Impresión de depuración
        return jsonify({"data": data})
    else:
        print("No se pudo conectar al SAM")  # Impresión de depuración
        return jsonify({"error": "No se pudo conectar al SAM"})


@app.route('/add_machine', methods=['POST'])
async def add_machine():
    data = await request.get_json()
    conn = await asyncpg.connect(**db_config)
    query = '''INSERT INTO maquina(nombre, ubicacion, descripcion, sensores)
               VALUES($1, $2, $3, $4) RETURNING id;'''
    values = (data['nombre'], data['ubicacion'], data['descripcion'], data['sensores'])
    new_machine_id = await conn.fetchval(query, *values)
    await conn.close()
    return jsonify({"new_machine_id": new_machine_id}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)