'''Proyecto sobre el sistema de gestion de cupos universitarios'''
import abc
class Usuario(metaclass=abc.ABCMeta):#Clase abstracta Usuario
    def __init__(self, cedula_pasaporte, nombre, apellido, correo):#Atributos de la clase Usuario, que seran heredados por las clases hijas
        self.cedula_pasaporte = cedula_pasaporte
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
    @abc.abstractmethod#Metodo abstracto iniciar_sesion
    def iniciar_sesion(self):
        pass
    @abc.abstractmethod#Metodo abstracto cerrar_sesion
    def cerrar_sesion(self):
        pass
    def cargar_datos(self):#Metodo cargar_datos
        pass

class Administrador(Usuario):#Clase Hija Administrador de Usuario
    def __init__(self, cedula_pasaporte, nombre, apellido, correo, cargo)
        super().__init__(cedula_pasaporte, nombre, apellido, correo)#Atributos heredados de Usuario más el atributo cargo
        self.cargo = cargo
        print("Los datos del administrador fueron ingresados con exitos.")
    def iniciar_sesion(self):
        print(f"Bienvenido de vuelta, Administrador {self.nombre}.")
    def cerrar_sesion(self):
        print(f"Hasta luego, Administrador {self.nombre}.")
    
class Aspirante(Usuario):#Clase Hija Aspirante de Usuario
    def __init__(self, cedula_pasaporte, nombre, apellido, correo, telefono, titulo):
        super().__init__(cedula_pasaporte, nombre, apellido, correo)#Atributos heredados de Usuario más los atributos telefono y titulo
        self.telefono = telefono
        self.titulo = titulo
        print("Los datos del aspirante fueron ingresados con exitos.")
    def iniciar_sesion(self):
        print(f"Aspirante {self.nombre} ha iniciado sesión.")
    def cerrar_sesion(self):
        print(f"Aspirante {self.nombre} ha cerrado sesión.")

class Soporte(Usuario):#Clase Hija Soporte de Usuario
    def __init__(self, cedula_pasaporte, nombre, apellido, correo, telefono):
        super().__init__(cedula_pasaporte, nombre, apellido, correo)#Atributos heredados de Usuario más el atributo telefono
        self.telefono = telefono
        print("Los datos del soporte fueron ingresados con exitos.")
    def iniciar_sesion(self):
        print(f"Soporte {self.nombre} ha iniciado sesión.")
    def cerrar_sesion(self):
        print(f"Soporte {self.nombre} ha cerrado sesión.")
    
class Profesor(Usuario):#Clase Hija Profesor de Usuario
    def __init__(self, cedula_pasaporte, nombre, apellido, correo, facultad):
        super().__init__(cedula_pasaporte, nombre, apellido, correo)#Atributos heredados de Usuario más el atributo facultad
        self.facultad = facultad
        print("Los datos del profesor fueron ingresados con exitos.")
    def iniciar_sesion(self):
        print(f"Profesor {self.nombre} ha iniciado sesión.")
    def cerrar_sesion(self):
        print(f"Profesor {self.nombre} ha cerrado sesión.")
    
class Universidad():#Clase Universidad
    Pais = "Ecuador"
    def __init__(self, nombre, provincia, canton, direccion, enlace):
        self.nombre = nombre
        self.provincia = provincia
        self.canton = canton
        self.direccion = direccion
        self.enlace = enlace

class Oferta_Academica:#Clase Oferta_Academica
    def __init__(self, carrera, cantidad):
        self.carrera = carrera
        self.cantidad = cantidad
        
class Periodo:#Clase Periodo
    def __init__(self, Año_Lectivo, Semestre):#Atributos de la clase Periodo
        self.Año_Lectivo = Año_Lectivo
        self.Semestre = Semestre
        print("Los datos del periodo fueron ingresados con éxitos")
    def iniciar_periodo(self):#Metodo iniciar_periodo
        print(f"El periodo {self.Año_Lectivo} - {self.Semestre} ha iniciado.")
    def finalizar_periodo(self):#Metodo finalizar_periodo
        print(f"El periodo {self.Año_Lectivo} - {self.Semestre} ha finalizado.")

class Inscripcion:#Clase Inscripcion
    def __init__(self, carrera, facultad):
        self.carrera = carrera
        self.facultad = facultad

class Evaluacion:#Clase Evaluacion
    def __init__(self, tipo, puntaje, horario, modalidad):
        self.tipo = tipo
        self.puntaje = puntaje
        self.horario = horario 
        self.modalidad = modalidad

class Postulacion:#Clase Postulacion
    def __init__(self, carrera, nota_final):
        self.carrera = carrera
        self.nota_final = nota_final