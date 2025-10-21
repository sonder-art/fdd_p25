import sys

arch = "notas.txt"

try: 
	with open(arch, "r", encoding="utf-8") as f:
		contenido = f.read()
		print(contenido)

except FileNotFoundError:
	print(f"Error: el archivo 'notas.txt' no existe.")
	sys.exit(1)
