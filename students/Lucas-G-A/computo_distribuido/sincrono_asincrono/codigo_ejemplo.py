import asyncio

async def tarea(nombre):
    print(f"{nombre} - inicio")
    await asyncio.sleep(0)  # Yield control al event loop
    print(f"{nombre} - después de primer yield")
    await asyncio.sleep(0)  # Yield control nuevamente
    print(f"{nombre} - fin")

async def main():
    await asyncio.gather(tarea("A"), tarea("B"))

asyncio.run(main())