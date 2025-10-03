import sys
nombre_archivo = "notas.txt"
try:
	with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
		contenido = archivo.read()
		print(contenido)
except FileNotFoundError:
	print(f"Error: El archivo '{nombre_archivo}' no fue encontrado.")
	sys.exit(1)



