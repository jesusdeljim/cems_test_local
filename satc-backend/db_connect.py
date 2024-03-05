import asyncpg
import asyncio

db_config = {
    'host': '172.18.0.6',
    'port': '5432',
    'database': 'satc_database',
    'user': 'root',
    'password': 'root'
}

async def connect_to_db():
    conn = await asyncpg.connect(
        host=db_config['host'],
        port=db_config['port'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )
    return conn

async def fetch_data(conn):
    rows = await conn.fetch('SELECT * FROM datos_adquiridos')
    return rows

async def main():
    try:
        # Conectar a la base de datos
        conn = await connect_to_db()
        print("Conexión exitosa a la base de datos")
        
        # Obtener datos
        rows = await fetch_data(conn)
        for row in rows:
            print(row)
        
        # Cerrar la conexión
        await conn.close()
        print("Conexión cerrada")
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")

# Ejecutar la función principal en el bucle de eventos
loop = asyncio.get_event_loop()
loop.run_until_complete(main())