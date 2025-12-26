from abc import ABC#impotar ABCMeta
from abc import abstractmethod#importar abstractmethod
class Autenticable(ABC):#Interfaz Autenticable
    @abstractmethod#Método iniciar sesión
    def iniciar_sesion(self):
        pass
    @abstractmethod#Método notificar sede
    def cerrar_sesion(self):
        pass

class Notificador(ABC):
    @abstractmethod#Método notificar sede
    def notificar_sede(self, sede: str):
        pass

class Cargable(ABC):
    @abstractmethod#Método cargar datos
    def cargar_datos(self):
        pass

class SolicitudAsistencia(ABC):#Clase SolicitudAsistencia
    @abstractmethod#Método crear solicitud asistencia
    def crear_solicitud_asistencia(self, asunto: str):
        pass
    @abstractmethod#Método estado solicitud
    def estado_solicitud(self, estado: str):
        pass
class GestorSede(ABC):#Clase GestorSede
    @abstractmethod#Método notificar sede
    def notificar_sede(self, sede: str):
        pass
    @abstractmethod#Método imprimir documentación sede
    def imprimir_documentacion_sede(self, sede: str):
        pass

class Usuario(Autenticable):#Clase abstracta Usuario
    def __init__(self, cedula_pasaporte: str, nombre: str, apellido: str, correo: str):
        self.cedula_pasaporte = cedula_pasaporte
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
    def iniciar_sesion(self):#Valor por defecto para usuarios que no implementan autenticación
        raise NotImplementedError("Este usuario no implementa autenticación")
    def cerrar_sesion(self):#Valor por defecto para usuarios que no implementan autenticación
        raise NotImplementedError("Este usuario no implementa autenticación")

class ServicioAutenticacion:#Clase ServicioAutenticacion
    def crear_usuario(self, aspirante, usuario: str, contrasena: str):#Método crear usuario
        if usuario != aspirante.cedula_pasaporte:#Validar que el usuario sea igual a la cédula o pasaporte
            raise ValueError("El usuario debe ser igual a la cédula o pasaporte.")
        aspirante.usuario = usuario
        aspirante.contrasena = contrasena
    def iniciar_sesion(self, aspirante, usuario: str, contrasena: str):#Método iniciar sesión
        return usuario == aspirante.usuario and contrasena == aspirante.contrasena

class Administrador(Usuario, Notificador, Cargable):#Clase Hija Administrador de Usuario
    def __init__(self, cedula, nombre, apellido, correo, cargo):
        super().__init__(cedula, nombre, apellido, correo)
        self.cargo = cargo
    def iniciar_sesion(self):
        print(f"Bienvenido Administrador {self.nombre}")
    def cerrar_sesion(self):
        print(f"Hasta luego Administrador {self.nombre}")
    def notificar_sede(self, sede):
        print(f"Administrador {self.nombre} ha notificado la sede: {sede}")
    def cargar_datos(self):
        print("El administrador está cargando datos...")
    def generar_reporte_inscripciones(self, lista_aspirantes):#Método generar_reporte_inscripciones
        print("\n=== REPORTE DE INSCRIPCIONES ===")
        print(f"Administrador: {self.nombre} ({self.cargo})")
        print(f"Total aspirantes: {len(lista_aspirantes)}\n")
        if not lista_aspirantes:
            print("No hay aspirantes registrados.")
            return
        for a in lista_aspirantes:
            print(f"- {a.nombre} {a.apellido} ({a.cedula_pasaporte})")

class Aspirante(Usuario, Cargable, SolicitudAsistencia, GestorSede):#Clase Hija Aspirante de Usuario
    def __init__(self, cedula, nombre, apellido, correo, telefono, titulo, nota_grado):
        super().__init__(cedula, nombre, apellido, correo)
        self.telefono = telefono
        self.titulo = titulo
        self._nota_grado = None
        self.nota_grado = nota_grado
        self.usuario = None
        self.contrasena = None
    @property#Propiedad nota grado
    def nota_grado(self):
        return self._nota_grado
    @nota_grado.setter#Setter nota grado con validacion
    def nota_grado(self, valor):
        if not (0 <= valor <= 10):
            raise ValueError("La nota debe estar entre 0 y 10.")
        self._nota_grado = valor
    def iniciar_sesion(self):
        print(f"Aspirante {self.nombre} inició sesión.")
    def cerrar_sesion(self):
        print(f"Aspirante {self.nombre} cerró sesión.")
    def cargar_datos(self):
        print("El aspirante ha cargado sus datos.")
    def nacionalidad(self):#Método nacionalidad
        if self.cedula_pasaporte.isdigit() and len(self.cedula_pasaporte) == 10:
            return "Ecuatoriano"
        return "Extranjero"
    def crear_solicitud_asistencia(self, asunto):#Método crear solicitud asistencia
        print(f"Aspirante {self.nombre} creó una solicitud de asistencia sobre: '{asunto}'.")
    def estado_solicitud(self, estado):#Método estado solicitud
        estado = estado.upper().strip()
        opciones = {"ENVIADA", "EN PROCESO", "RESUELTA"}
        if estado not in opciones:
            print("Estado no válido. Use: ENVIADA | EN PROCESO | RESUELTA.")
        else:
            print(f"Solicitud de asistencia: {estado}")
    def notificar_sede(self, sede):#Método notificar sede
        print(f"Aspirante {self.nombre} ha notificado la sede: {sede}")
    def imprimir_documentacion_sede(self, sede):#Método imprimir documentación sede
        print(f"Aspirante {self.nombre} está imprimiendo documentación para la sede: {sede}")

class Soporte(Usuario):#Clase Hija Soporte de Usuario
    def __init__(self, cedula, nombre, apellido, correo, telefono):
        super().__init__(cedula, nombre, apellido, correo)
        self.telefono = telefono
    def iniciar_sesion(self):
        print(f"Soporte {self.nombre} inició sesión.")
    def cerrar_sesion(self):
        print(f"Soporte {self.nombre} cerró sesión.")
    def recibir_asistencia(self, aspirante):#Método recibir asistencia
        print(f"Soporte {self.nombre} atendiendo a {aspirante.nombre}...")
    def estado_asistencia(self, estado):#Método estado asistencia
        estado = estado.upper().strip()
        opciones = {"RESUELTA", "RECHAZADA", "PROCESO"}
        if estado not in opciones:
            print("Estado no válido. Use: RESUELTA | RECHAZADA | PROCESO.")
        else:
            print(f"Asistencia: {estado}")

class Profesor(Usuario):#Clase Hija Profesor de Usuario
    def __init__(self, cedula, nombre, apellido, correo, facultad):
        super().__init__(cedula, nombre, apellido, correo)
        self.facultad = facultad
    def iniciar_sesion(self):
        print(f"Profesor {self.nombre} inició sesión.")
    def cerrar_sesion(self):
        print(f"Profesor {self.nombre} cerró sesión.")
    def crear_cuestionario(self, tema, cantidad):#Método crear cuestionario
        print(f"Profesor {self.nombre} creó un cuestionario de '{tema}' con {cantidad} preguntas.")


