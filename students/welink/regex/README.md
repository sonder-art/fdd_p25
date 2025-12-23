# Tarea 08: Expresiones Regulares

Esta carpeta contiene la evidencia de la Tarea 08.

## Ejercicios con Grep (Terminal)

```bash
# Buscar palabras que empiecen con mayúscula
grep -E "\b[A-Z][a-z]*\b" archivo.txt

# Buscar correos electrónicos válidos
grep -E "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}" archivo.txt

# Buscar números de teléfono (formato simple 123-456-7890)
grep -E "\b\d{3}-\d{3}-\d{4}\b" archivo.txt
```

## Ejercicios con Python

El archivo `regex_test.py` contiene la implementación de las funciones solicitadas:
1.  `validar_email`
2.  `extraer_fechas`
3.  `censurar_palabras`

Para ejecutarlo:
```bash
python3 regex_test.py
```
