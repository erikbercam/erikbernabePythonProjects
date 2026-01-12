import requests

BASE_URL = "http://127.0.0.1:5000/api/books"


def run_test():
    print("--- Pruebas ---")


    nuevo_libro = {
        "title": "La sombra del viento",
        "author": "Carlos Ruiz Ber",
        "price": 22.50
    }

    response = requests.post(BASE_URL, json=nuevo_libro)
    print(f"\n1. POST (Crear): Estado {response.status_code}")
    print(f"Respuesta: {response.json()}")


    book_id = 4


    response = requests.get(BASE_URL)
    print(f"\n2. GET (Lista completa): Estado {response.status_code}")
    print(f"Libros en BD: {response.json()}")


    update_data = {"title": "La sombra del viento premium"}
    response = requests.put(f"{BASE_URL}/{book_id}", json=update_data)
    print(f"\n3. PUT (Actualizar ID {book_id}): Estado {response.status_code}")
    print(f"Respuesta: {response.json()}")


    response = requests.delete(f"{BASE_URL}/{book_id}")
    print(f"\n4. DELETE (Borrar ID {book_id}): Estado {response.status_code}")
    if response.status_code == 204:
        print("Libro eliminado.")


if __name__ == "__main__":
    try:
        run_test()
    except Exception as e:
        print(f"Revisa si se esta ejecutando. {e}")