import psycopg2

# Configura los parámetros de conexión a la base de datos
db_config = {
    'host': '172.18.0.6', #Ip del contenedor de la base de datos
    'port': '54321',
    'database': 'satc_database',
    'user': 'root',
    'password': 'root'
}

# Conecta a la base de datos
try:
    conn = psycopg2.connect(**db_config)
    print("Conexión exitosa a la base de datos")
except (Exception, psycopg2.Error) as error:
    print("Error al conectar a la base de datos:", error)

# Crear un cursor
cursor = conn.cursor()

# Ejecutar una consulta SQL
cursor.execute("SELECT * FROM datos_adquiridos")

# Obtener los resultados de la consulta
rows = cursor.fetchall()

# Imprimir los resultados
for row in rows:
    print(row)

# Cerrar el cursor y la conexión
cursor.close()
conn.close()
