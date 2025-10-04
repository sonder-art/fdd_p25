import sys

nombre_archivo = 'notas.txt'

try:
	with open(nombre_archivo, 'r') as archivo:
		contenido = archivo.read()
		print(contenido)
except:
	print(f"Error el archivo '{nombre_archivo}' no se econtró")
	sys.exit(1)
