from asyncua import Client
import asyncio

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
        data = {}
        for var in variables:
            value = await var.read_value()
            browse_name = await var.read_browse_name()
            # Usa el atributo Name del browse_name para obtener el nombre del nodo
            data[browse_name.Name] = value
        return data
    except Exception as e:
        print(f"Error al leer las variables del objeto {object_node_id}: {e}")
        return None