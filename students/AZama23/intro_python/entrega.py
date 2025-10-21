import sys
file = "notas.txt"

try:
	with open(file, "r", encoding="utf-8") as f:
		res = f.read()
		print(res)

except FileNotFoundError:
	print("error, no se encontro el archivo notas.txt")
	sys.exit(1)
