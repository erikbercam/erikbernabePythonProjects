from dominio.alumno import Alumno
from servicio.alumnos_matriculados import AlumnosMatriculados

def mostrar_menu():
    print('\nMenú Matriculacion Erik Bernabe')
    print('1. Matricular Alumno')
    print('2. Listar Alumnos')
    print('3. Eliminar Archivo de Alumnos')
    print('4. Salir')
def ejecutar_app():
    while True:
        mostrar_menu()
        opcion = input('Escoge: ')
        if opcion == '1':
            nombre_alumno = input('Ingrese el nombre del alumno a matricular: ')
            alumno = Alumno(nombre_alumno)
            AlumnosMatriculados.matricular_alumno(alumno)
        elif opcion == '2':
            AlumnosMatriculados.listar_alumnos()
        elif opcion == '3':
            confirmacion = input('Quieres eliminar el archivo? (s/n): ').lower()
            if confirmacion == 's':
                AlumnosMatriculados.eliminar_alumnos()
            else:
                print('Operacion cancelada.')
        elif opcion == '4':
            print(' Adeeeeeuuuuuu...')
            break
        else:
            print('Introduce una opcion valida.')

if __name__ == '__main__':
    ejecutar_app()