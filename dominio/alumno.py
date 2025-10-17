class Alumno:

    def __init__(self, nombre):
        self._nombre = nombre

    def __str__(self):

        return f'Alumno: {self.nombre}'

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nombre):
        self._nombre = nombre