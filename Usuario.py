from abc import ABC#impotar ABCMeta
from abc import abstractmethod#importar abstractmethod
class Usuario(ABC):#Clase abstracta Usuario
    def __init__(self, cedula_pasaporte: str, nombre:str, apellido:str, correo:str):#Atributos de la clase Usuario, que seran heredados por las clases hijas
        self.cedula_pasaporte = cedula_pasaporte
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
    @abstractmethod#Metodo abstracto iniciar_sesion
    def iniciar_sesion(self):
        pass
    @abstractmethod#Metodo abstracto cerrar_sesion
    def cerrar_sesion(self):
        pass
    def crear_usuario(self):#Metodo crear_usuario
        pass
    def cargar_datos(self):#Metodo cargar_datos
        pass
    def notificar_sede(self):#Metodo notificar_sede
        pass

class Administrador(Usuario):#Clase Hija Administrador de Usuario
    def __init__(self, cedula_pasaporte:str, nombre:str, apellido:str, correo:str, cargo:str):
        super().__init__(cedula_pasaporte, nombre, apellido, correo)#Atributos heredados de Usuario más el atributo cargo
        self.cargo = cargo
        print("Los datos del administrador fueron ingresados con exitos.")
    def iniciar_sesion(self):#Metodo iniciar_sesion
        print(f"Bienvenido, Administrador {self.nombre}.")
    def cerrar_sesion(self):#Metodo cerrar_sesion
        print(f"Hasta luego, Administrador {self.nombre}.")
    def cargar_datos(self):#Metodo cargar_datos
        print(f"El administrador creo la opcion de cargar datos para los usuarios.")
    def generar_reporte_inscripciones(self, lista_aspirantes): #Método generar_reporte_inscripciones
        print(f"Reporte de Inscripciones")
        print(f"Administrador: {self.nombre} ({self.cargo})")
        print(f"Total de aspirantes inscritos: {len(lista_aspirantes)}\n")
        if not lista_aspirantes:
            print("No hay aspirantes registrados actualmente")
            return
        for i in lista_aspirantes:
            print(f"- {i.nombre} {i.apellido} ({i.cedula_pasaporte}) - {i.correo}")  
    def notificar_sede(self, sede: str):  # Método notificar_sede
        print(f"El administrador {self.nombre} ha notificado las sedes {sede} para que los aspirantes rindan la evaluación.")
    
class Aspirante(Usuario):#Clase Hija Aspirante de Usuario
    def __init__(self, cedula_pasaporte:str, nombre:str, apellido:str, correo:str, telefono:str, titulo:bool, nota_grado:float):
        super().__init__(cedula_pasaporte, nombre, apellido, correo)#Atributos heredados de Usuario más los atributos telefono y titulo
        self.telefono = telefono
        self.titulo = titulo
        self.nota_grado = nota_grado
        self.usuario = None
        self.contrasena = None
        print("Los datos del aspirante fueron ingresados con éxitos.")
    
    def crear_usuario(self):#Metodo crear_usuario
        while True:#Bucle para validar la creacion del usuario
            try:#Validar que los datos ingresados sean correctos
                usuario = input("Ingrese su usuario (cédula o pasaporte): ")
                contrasena = input("Ingrese su contraseña: ")
                contrasena_confirmar = input("Confirme su contraseña: ")
                if usuario != self.cedula_pasaporte:#Validacion de usuario
                    raise ValueError("El usuario debe ser igual a la cédula o pasaporte.")
                if contrasena != contrasena_confirmar: #Validacion de contraseñas
                    raise ValueError("Las contraseñas no coinciden.")
                self.usuario = usuario#Validar que el usuario y la contraseña se asignen correctamente
                self.contrasena = contrasena
                print(f"El aspirante {self.nombre} ha creado su usuario con éxito.")
                break #Salir del bucle si todo es correcto
            except ValueError as error:#Captura de errores y muestra el mensaje correspondiente
                print(f"Error: {error}. Intente de nuevo.")

    def iniciar_sesion(self):#Metodo iniciar_sesion
        if self.usuario is None or self.contrasena is None:#Verifica si el usuario ha creado un usuario
            print("El aspirante debe crear un usuario antes de iniciar sesión.")
            return False
        while True:#Bucle para validar el inicio de sesion
            usuario = input("Ingrese su usuario: ")
            contrasena = input("Ingrese su contraseña: ")
            if usuario == self.usuario and contrasena == self.contrasena:#Validacion de usuario y contraseña
                print(f"Aspirante {self.nombre} ha iniciado sesión con éxito.")
                return True
            else:#Mensaje de error si los datos son incorrectos
                print("Usuario o contraseña incorrectos. Intente de nuevo.")
                salir = input("¿Desea intentar de nuevo? (SI/NO): ").upper()#Pregunta para salir del bucle
                if salir == 'NO':#Salir del bucle si el usuario no desea intentar de nuevo
                    print("Se canceló el inicio de sesión.")
                    return False

    def cerrar_sesion(self):#Metodo cerrar_sesion
        print(f"Aspirante {self.nombre} ha cerrado sesión.")
    @property
    def nota_grado(self):#Getter nota_grado
        return self._nota_grado
    @nota_grado.setter
    def nota_grado(self, valor:float):#Setter nota_grado con validacion
        if (valor < 0) or (valor > 10):
            raise ValueError("La nota de grado no puede ser negativa o mayor a diez.")
        self._nota_grado = valor
    def nacionalidad(self):#Metodo nacionalidad
        if self.cedula_pasaporte.isdigit() and len(self.cedula_pasaporte) == 10:
            return "Ecuatoriano"
        else:
            return "Extranjero" 
    def cargar_datos(self):#Metodo cargar_datos
        print(f"El aspirante ha subido con éxito la información requerida.")
    def notificar_sede(self):#Metodo notificar_sede
        print(f"El aspirante {self.nombre} ha notificado a la sede correspondiente.")

class Soporte(Usuario):#Clase Hija Soporte de Usuario
    def __init__(self, cedula_pasaporte:str, nombre:str, apellido:str, correo:str, telefono:str):
        super().__init__(cedula_pasaporte, nombre, apellido, correo)#Atributos heredados de Usuario más el atributo telefono
        self.telefono = telefono
        print("Los datos del soporte fueron ingresados con éxitos.")
    def iniciar_sesion(self):#Metodo iniciar_sesion
        print(f"Soporte {self.nombre} ha iniciado sesión.")
    def cerrar_sesion(self):#Metodo cerrar_sesion
        print(f"Soporte {self.nombre} ha cerrado sesión.")
    def recibir_asistencia(self, aspirante):#Metodo recibir_asistencia
        print(f"Soporte {self.nombre} está atendiendo la solicitud de asistencia del aspirante {aspirante.nombre}.")
    def estado_asistencia(self,estado:str):#Metodo estado_asistencia
        if not isinstance(estado, str):#Verifica que el estado sea una cadena de texto
            raise ValueError("El estado debe ser una cadena de texto.")
        estado=estado.upper().strip()#Normaliza el estado a mayusculas y elimina espacios en blanco
        if estado == "RESUELTA":#Verifica el estado de la asistencia    
            print("La asistencia ha sido resuelta.")
        elif estado == "RECHAZADA":
            print("La asistencia ha sido rechazada.")
        elif estado == "PROCESO":
            print("La asistencia está en proceso.")
        else:
            print("Estado no válido. Usa: 'RESUELTA', 'RECHAZADA' o 'PROCESO'.")
    
class Profesor(Usuario):#Clase Hija Profesor de Usuario
    def __init__(self, cedula_pasaporte:str, nombre:str, apellido:str, correo:str, facultad:str):
        super().__init__(cedula_pasaporte, nombre, apellido, correo)#Atributos heredados de Usuario más el atributo facultad
        self.facultad = facultad
        print("Los datos del profesor fueron ingresados con éxitos.")
    def iniciar_sesion(self):#Metodo iniciar_sesion
        print(f"Profesor {self.nombre} ha iniciado sesión.")
    def cerrar_sesion(self):#Metodo cerrar_sesion
        print(f"Profesor {self.nombre} ha cerrado sesión.")
    def crear_cuestionario(self, tema:str, numero_preguntas:int):#Metodo crear_cuestionario
        print(f"El profesor {self.nombre} ha creado un cuestionario sobre {tema} con {numero_preguntas} preguntas.")
