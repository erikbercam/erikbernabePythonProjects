import csv
import os


def fusionar_notas(archivo_uf1, archivo_uf2, archivo_salida):
    """
    Lee los datos de los alumnos de dos archivos CSV, fusiona las notas,
    y escribe los datos combinados en un nuevo archivo CSV.

    Args:
        archivo_uf1 (str): La ruta al archivo CSV para las notas de UF1.
        archivo_uf2 (str): La ruta al archivo CSV para las notas de UF2.
        archivo_salida (str): La ruta al archivo CSV de salida.
    """
    # Diccionario para almacenar los datos fusionados
    notas_alumnos = {}

    # --- Leer y procesar el primer archivo (UF1) ---
    try:
        with open(archivo_uf1, mode='r', newline='', encoding='utf-8') as csvfile1:
            lector1 = csv.DictReader(csvfile1, delimiter=';')
            # Limpiar los nombres de las columnas que puedan tener espacios extra
            lector1.fieldnames = [field.strip() for field in lector1.fieldnames]
            for fila in lector1:
                id_alumno = fila['Id']
                notas_alumnos[id_alumno] = {
                    'Apellidos': fila['Apellidos'],
                    'Nombre': fila['Nombre'],
                    'UF1': fila['UF1'],
                    'UF2': None  # Inicializar la nota de UF2
                }
    except FileNotFoundError:
        print(f"Error: El archivo {archivo_uf1} no fue encontrado.")
        return
    except Exception as e:
        print(f"Ocurrió un error al leer {archivo_uf1}: {e}")
        return

    # --- Leer y procesar el segundo archivo (UF2) ---
    try:
        with open(archivo_uf2, mode='r', newline='', encoding='utf-8') as csvfile2:
            lector2 = csv.DictReader(csvfile2, delimiter=';')
            # Limpiar los nombres de las columnas que puedan tener espacios extra
            lector2.fieldnames = [field.strip() for field in lector2.fieldnames]
            for fila in lector2:
                id_alumno = fila['Id']
                if id_alumno in notas_alumnos:
                    notas_alumnos[id_alumno]['UF2'] = fila['UF2']
    except FileNotFoundError:
        print(f"Error: El archivo {archivo_uf2} no fue encontrado.")
        return
    except Exception as e:
        print(f"Ocurrió un error al leer {archivo_uf2}: {e}")
        return

    # --- Escribir los datos fusionados en el archivo de salida ---
    nombres_campos = ['Id', 'Apellidos', 'Nombre', 'UF1', 'UF2']
    try:
        with open(archivo_salida, mode='w', newline='', encoding='utf-8') as csv_salida:
            escritor = csv.DictWriter(csv_salida, fieldnames=nombres_campos, delimiter=';')
            escritor.writeheader()
            # Ordenar por Id de alumno antes de escribir
            for id_alumno, datos in sorted(notas_alumnos.items(), key=lambda item: int(item[0])):
                escritor.writerow({
                    'Id': id_alumno,
                    'Apellidos': datos['Apellidos'],
                    'Nombre': datos['Nombre'],
                    'UF1': datos['UF1'],
                    'UF2': datos['UF2']
                })
        print(f"Se ha creado el archivo {archivo_salida} con éxito.")
    except Exception as e:
        print(f"Ocurrió un error al escribir en {archivo_salida}: {e}")


# --- Ejecución principal ---
if __name__ == "__main__":
    # Crear un directorio 'data' si no existe
    if not os.path.exists('data'):
        os.makedirs('data')

    # Definir rutas de los archivos (usando los nombres que subiste)
    archivo_uf1 = 'data/Notas_Alumnos_UF1 (1).csv'
    archivo_uf2 = 'data/Notas_Alumnos_UF2 (1).csv'
    archivo_salida = 'data/notas_alumnos.csv'

    # Ejecutar la función de fusión
    fusionar_notas(archivo_uf1, archivo_uf2, archivo_salida)