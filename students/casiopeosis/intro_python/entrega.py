try:
	with open("notas.txt", "r") as file:
		contenido = file.read()
		print(contenido)
except FileNotFoundError:
	print("No hay 'notas.txt'")
except Exception as e:
	print("Error: ", {e})
