import re

def validar_email(email):
    """Valida si un string es un email válido."""
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(patron, email))

def extraer_fechas(texto):
    """Extrae todas las fechas en formato dd/mm/yyyy."""
    patron = r'\b\d{2}/\d{2}/\d{4}\b'
    return re.findall(patron, texto)

def censurar_palabras(texto, prohibidas):
    """Sustituye palabras prohibidas por asteriscos."""
    for palabra in prohibidas:
        patron = r'\b' + re.escape(palabra) + r'\b'
        texto = re.sub(patron, '*' * len(palabra), texto, flags=re.IGNORECASE)
    return texto

if __name__ == "__main__":
    # Test validar_email
    print(f"test@example.com: {validar_email('test@example.com')}")
    print(f"invalid-email: {validar_email('invalid-email')}")

    # Test extraer_fechas
    texto_fechas = "La reunión es el 12/05/2025 y la entrega el 20/05/2025."
    print(f"Fechas encontradas: {extraer_fechas(texto_fechas)}")

    # Test censurar_palabras
    texto_censura = "Este es un mensaje con palabras prohibidas como tonto y feo."
    prohibidas = ["tonto", "feo"]
    print(f"Texto censurado: {censurar_palabras(texto_censura, prohibidas)}")
