import sys

try:
	with open('notas.txt', encoding="utf-8") as nota:
		read_nota = nota.read()
		print(read_nota)
except FileNotFoundError as e:
	print ("Error: El archivo no existe")
	sys.exit(1)
