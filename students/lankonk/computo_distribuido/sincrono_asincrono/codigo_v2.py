import asyncio

# Esto es una corrutina (función asíncrona)
async def tarea_simple():
    print("Inicio de la tarea")
    await asyncio.sleep(1)  # Simula una espera (wait)
    print("Fin de la tarea")

asyncio.run(tarea_simple())