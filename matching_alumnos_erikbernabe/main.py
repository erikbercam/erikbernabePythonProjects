import csv
import os


file_uf1 = 'Notas_Alumnos_UF1.csv'
file_uf2 = 'Notas_Alumnos_UF2.csv'
file_output = 'notas_alumnos.csv'


datos_alumnos = {}

try:
    
   
    with open(file_uf1, mode='r', encoding='latin-1') as f:
        reader_uf1 = csv.DictReader(f, delimiter=';')

        for fila in reader_uf1:
            datos_alumnos[fila['Id']] = fila

   
    with open(file_uf2, mode='r', encoding='latin-1') as f:
        reader_uf2 = csv.DictReader(f, delimiter=';')

        for fila in reader_uf2:
            alumno_id = fila['Id']
            if alumno_id in datos_alumnos:
                datos_alumnos[alumno_id]['UF2'] = fila['UF2']
            else:
                print(f"Advertencia: Alumno con Id {alumno_id} no encontrado en {file_uf1}")

    fieldnames = ['Id', 'Apellidos', 'Nombre', 'UF1', 'UF2']
    
    with open(file_output, mode='w', encoding='utf-8', newline='') as f:

        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')

        writer.writeheader()

        writer.writerows(datos_alumnos.values())

    print(f"¡Éxito! Se ha creado el archivo '{file_output}' correctamente.")
    print(f"Se procesaron {len(datos_alumnos)} alumnos.")

except FileNotFoundError as e:
    print(f"Error: No se encontró el archivo {e.filename}.")
except Exception as e:
    # Esto imprimirá el error de forma más clara si vuelve a pasar
    print(f"Ha ocurrido un error inesperado: {type(e).__name__} - {e}")
