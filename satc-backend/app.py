from quart import Quart, jsonify
from opcua_client import connect_to_sam, disconnect_from_sam, read_data_from_sam

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)