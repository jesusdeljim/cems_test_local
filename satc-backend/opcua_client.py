from asyncua import Client, Node
from asyncua.common.subscription import Subscription, DataChangeNotificationHandler
import asyncio
from datetime import datetime
import asyncpg

class MyDataChangeHandler(DataChangeNotificationHandler):
    async def datachange_notification(self, node, val, data):
        try:
            print(f"Valor del sensor actualizado: {val}")
            timestamp = datetime.now()
            browse_name = await node.read_browse_name()
            
            conn = await asyncpg.connect(**db_config)
            sensor = await conn.fetchrow(
                'SELECT id, tipo, maquina_id FROM sensor WHERE nombre = $1;', browse_name.Name
            )
            print(f"Sensor encontrado: {sensor}")
            if sensor:
                await conn.execute(
                    '''INSERT INTO datos_adquiridos(timestamp, variable, valor, sensor_id, maquina_id)
                    VALUES($1, $2, $3, $4, $5);''',
                    timestamp, sensor['tipo'], val, sensor['id'], sensor['maquina_id']
                )
                print(f"Dato insertado en la base de datos para el sensor {browse_name.Name}")
            else:
                print(f"No se encontró el sensor con nombre {browse_name.Name} en la base de datos")
            await conn.close()
        except Exception as e:
            print(f"Error al manejar la notificación de cambio de datos: {e}")


db_config = {
    'host': '172.18.0.6',
    'port': '5432',
    'database': 'satc_database',
    'user': 'root',
    'password': 'root'
}

async def connect_to_sam(server_url):
    try:
        client = Client(server_url)
        await client.connect()
        print("Conexión exitosa con el SAM.")
        return client
    except Exception as e:
        print("Error al conectar con el SAM:", e)
        return None

async def disconnect_from_sam(client):
    try:
        await client.disconnect()
        print("Desconectado del SAM.")
    except Exception as e:
        print("Error al desconectar del SAM:", e)

async def read_data_from_sam(client, object_node_id):
    try:
        object_node = client.get_node(object_node_id)
        variables = await object_node.get_variables()
        data = []
        for var in variables:
            value = await var.read_value()
            browse_name = await var.read_browse_name()
            timestamp = datetime.now()  # Genera el timestamp actual
            
            # Obtener sensor_id y maquina_id de la base de datos basado en el browse_name
            conn = await asyncpg.connect(**db_config)
            sensor = await conn.fetchrow(
                'SELECT id, tipo, maquina_id FROM sensor WHERE nombre = $1;', browse_name.Name
            )
            await conn.close()

            if sensor:
                data.append({
                    'timestamp': timestamp,
                    'variable': sensor['tipo'],
                    'valor': value,
                    'sensor_id': sensor['id'],
                    'maquina_id': sensor['maquina_id']
                })
            else:
                print(f"No se encontró el sensor con nombre {browse_name.Name} en la base de datos")
        return data
    except Exception as e:
        print(f"Error al leer las variables del objeto {object_node_id}: {e}")
        return None


async def main():
    server_url = "opc.tcp://opcua_server:4840"  # Asegúrate de que la URL esté correcta
    client = await connect_to_sam(server_url)
    if client:
        handler = MyDataChangeHandler()
        subscription = await client.create_subscription(1000, handler)
        object_node_id = "ns=2;i=1"  # Reemplaza esto con el NodeId del objeto que contiene las variables
        object_node = client.get_node(object_node_id)
        variables = await object_node.get_variables()
        for var in variables:
            await subscription.subscribe_data_change(var)
        print("Suscripción a cambios de valor de sensores configurada.")
        # Mantener la suscripción activa
        try:
            while True:
                await asyncio.sleep(1)
        finally:
            # Cancelar la suscripción y desconectar del servidor OPC UA
            await subscription.delete()
            await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())