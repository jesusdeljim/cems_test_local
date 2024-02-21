from asyncua import Server
import asyncio

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

    # Obtiene el nodo de objetos y agrega tus nodos aquí
    myobj = await server.nodes.objects.add_object(idx, "MyObject")
    myvar = await myobj.add_variable(idx, "MyVariable", 42)  # Agrega una variable con valor inicial 42
    await myvar.set_writable()  # Hace la variable escribible
    # Añade otra variable al mismo objeto
    myvar2 = await myobj.add_variable(idx, "AnotherVariable", 73)  # Agrega otra variable con valor inicial 73
    await myvar2.set_writable()  # Hace la nueva variable escribible

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