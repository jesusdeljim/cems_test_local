from asyncua import Server, ua
import asyncio
import asyncpg
from datetime import datetime


db_config = {
    'host': '172.18.0.6',
    'port': '5432',
    'database': 'satc_database',
    'user': 'root',
    'password': 'root'
}

async def add_sensors_to_opc_server(server, idx):
    # Conectarse a la base de datos y obtener los sensores
    conn = await asyncpg.connect(**db_config
    )
    sensors = await conn.fetch('SELECT * FROM sensor;')
    await conn.close()

    # Objeto OPC para contener las variables de los sensores
    sensors_obj = await server.nodes.objects.add_object(idx, "Sensors")

    # Añadir cada sensor como una variable OPC
    for sensor in sensors:
        sensor_name = sensor['nombre']
        sensor_value = 0  # Asumiendo un valor inicial de 0 para los sensores
        sensor_var = await sensors_obj.add_variable(idx, sensor_name, sensor_value)
        await sensor_var.set_writable()  # Hace la variable escribible si es necesario

async def main():
    # Crea una instancia del servidor OPC UA
    server = Server()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

    # Inicializa el servidor antes de registrar espacios de nombres o crear nodos
    await server.init()

    # Registra un nuevo espacio de nombres
    uri = "http://ejemplo.org/espacio-de-nombres-de-prueba"
    idx = await server.register_namespace(uri)

    print(f"Índice del espacio de nombres registrado: {idx}")

    # Añade los sensores como variables OPC
    await add_sensors_to_opc_server(server, idx)

    # Inicia el servidor
    await server.start()
    print("Servidor OPC UA iniciado en el puerto 4840")

    # Mantiene el servidor en ejecución
    try:
        while True:
            await asyncio.sleep(1)
    finally:
        # Cierra el servidor al finalizar
        await server.stop()

if __name__ == '__main__':
    asyncio.run(main())