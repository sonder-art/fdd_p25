import requests

def main():
    print("Probando requests dentro del entorno virtual...")
    try:
        response = requests.get("https://api.github.com")
        print(f"Status Code de GitHub API: {response.status_code}")
        print("¡Éxito! La librería requests está instalada y funcionando.")
    except ImportError:
        print("Error: La librería requests no está instalada.")

if __name__ == "__main__":
    main()
