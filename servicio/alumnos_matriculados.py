from dominio.alumno import Alumno
import os

class AlumnosMatriculados:

    ruta_archivo = 'alumnos.txt'

    @classmethod
    def matricular_alumno(cls, alumno: Alumno):

        with open(cls.ruta_archivo, 'a', encoding='utf8') as archivo:
            archivo.write(f'{alumno.nombre}\n')
        print(f'Alumno "{alumno.nombre}" matriculado correctamente.')

    @classmethod
    def listar_alumnos(cls):

        try:
            with open(cls.ruta_archivo, 'r', encoding='utf8') as archivo:
                print('Listado de Alumnos:')
                contenido = archivo.read()
                if contenido:
                    print(contenido, end='')
                else:
                    print('No hay alumnos matriculados.')
        except FileNotFoundError:

            print('No hay aun alumnos matriculados.')

    @classmethod
    def eliminar_alumnos(cls):

        try:

            os.remove(cls.ruta_archivo)
            print(' Archivo eliminado.')
        except FileNotFoundError:
            print('El archivo no existe.')