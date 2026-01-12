from abc import ABC#importar ABCMeta
from abc import abstractmethod#importar abstractmethod
import json#importar json
import os#importar os
from datetime import date, timedelta#importar date para manejo de fechas

class Autenticable(ABC):#Interfaz Autenticable
    @abstractmethod#Método iniciar sesión
    def iniciar_sesion(self):
        pass
    @abstractmethod#Método cerrar sesión
    def cerrar_sesion(self):
        pass

class AsignarSede(ABC):#Interfaz AsignarSede
    @abstractmethod#Método asignar sede
    def asignar_sede(self, sede: str):
        pass

class Cargable(ABC):#Interfaz Cargable
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

class GestionProceso(ABC):#Clase GestionProceso
    @abstractmethod#Método abrir inscripciones
    def abrir_inscripciones(self, fecha_inicio: date, fecha_fin: date):
        pass
    @abstractmethod#Método cerrar inscripciones
    def cerrar_inscripciones(self):
        pass
    @abstractmethod#Método inscripciones activas
    def inscripciones_activas(self):
        pass
    @abstractmethod#Método abrir evaluación
    def abrir_evaluaciones(self, fecha_inicio: date, fecha_fin: date):
        pass
    @abstractmethod#Método cerrar evaluación
    def cerrar_evaluaciones(self):
        pass
    @abstractmethod#Método evaluación activa
    def evaluaciones_activas(self):
        pass
    @abstractmethod#Método abrir postulaciones
    def abrir_postulaciones(self, fecha_inicio: date, fecha_fin: date):
        pass
    @abstractmethod#Método cerrar postulaciones
    def cerrar_postulaciones(self):
        pass
    @abstractmethod#Método postulaciones activas
    def postulaciones_activas(self):
        pass

class Usuario(Autenticable, ABC):#Clase abstracta Usuario
    def __init__(self, cedula_pasaporte: str, nombre: str, apellido: str, correo: str):
        self.cedula_pasaporte = cedula_pasaporte
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
    def iniciar_sesion(self):#Valor por defecto para usuarios que no implementan autenticación
        raise NotImplementedError("Este usuario no implementa autenticación")
    def cerrar_sesion(self):#Valor por defecto para usuarios que no implementan autenticación
        raise NotImplementedError("Este usuario no implementa autenticación")

class RepositorioAspirantes(ABC):#Interfaz Repositorio
    @abstractmethod#Método leer datos
    def leer_todos(self):
        pass
    @abstractmethod#Método guardar datos
    def guardar_todos(self, datos):
        pass

class RepositorioAspirantesJSON(RepositorioAspirantes):#Repositorio JSON
    def __init__(self, archivo="aspirantes_universidad.json"):#Leer archivo JSON
        base_dir = os.path.dirname(os.path.abspath(__file__))#Directorio base
        self.archivo = os.path.join(base_dir, archivo)
        if not os.path.exists(self.archivo):#Crear archivo si no existe
            with open(self.archivo, "w", encoding="utf-8") as f:
                json.dump([], f)
    def leer_todos(self):#Leer base de datos
        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print("ERROR EN EL JSON:", e)
            raise
    def guardar_todos(self, datos):#Guardar base de datos
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

class ServicioAutenticacion:#Clase ServicioAutenticacion
    def __init__(self, repositorio: RepositorioAspirantes):
        self.repositorio = repositorio
    def crear_usuario(self, cedula, usuario: str, contrasena: str):#Método crear usuario
        if not contrasena:
            raise ValueError("La contraseña no puede estar vacía")
        aspirantes = self.repositorio.leer_todos()
        for a in aspirantes:#Buscar aspirante por cédula
            if a["numero_identidad"] == cedula:
                if "usuario" in a:
                    raise ValueError("El usuario ya existe")
                if usuario != cedula:# Validar que el usuario sea igual a la cédula o pasaporte
                    raise ValueError("El usuario debe ser igual a la cédula o pasaporte")
                a["usuario"] = usuario
                a["contrasena"] = contrasena
                self.repositorio.guardar_todos(aspirantes)
                print("Usuario creado correctamente")
                return
        raise ValueError("No existe aspirante con esa identificación")
    def iniciar_sesion(self, usuario: str, contrasena: str):#Método iniciar sesión
        aspirantes = self.repositorio.leer_todos()
        for a in aspirantes:#Buscar usuario y contraseña
            if a.get("usuario") == usuario and a.get("contrasena") == contrasena:
                print("Inicio de sesión exitoso")
                return True
        print("Credenciales incorrectas")
        return False

class ServicioRecuperacion:#Servicio recuperación contraseña
    def __init__(self, repositorio: RepositorioAspirantes):
        self.repositorio = repositorio
    def cambiar_contrasena_por_correo(self, correo, nueva_contrasena):#Método cambiar contraseña
        aspirantes = self.repositorio.leer_todos()
        for a in aspirantes:
            if a["correo"] == correo:
                a["contrasena"] = nueva_contrasena
                self.repositorio.guardar_todos(aspirantes)
                print("Contraseña actualizada correctamente")
                return
        raise ValueError("Correo no registrado")
    
class SistemaFacade:#Clase Fachada del sistema
    def __init__(self):
        self.repo = RepositorioAspirantesJSON()
        self.auth = ServicioAutenticacion(self.repo)
        self.recuperacion = ServicioRecuperacion(self.repo)
    def registrar_usuario(self, cedula, usuario, contrasena):#Registrar usuario
        self.auth.crear_usuario(cedula, usuario, contrasena)
    def login(self, usuario, contrasena):#Iniciar sesión
        return self.auth.iniciar_sesion(usuario, contrasena)
    def recuperar_contrasena(self, correo, nueva):#Recuperar contraseña
        self.recuperacion.cambiar_contrasena_por_correo(correo, nueva)

class Administrador(Usuario, AsignarSede, Cargable, GestionProceso):#Clase Hija Administrador de Usuario
    def __init__(self, cedula, nombre, apellido, correo, cargo):
        super().__init__(cedula, nombre, apellido, correo)
        self.cargo = cargo
        self.fases = {# Diccionario de fases y secuencia
            "inscripcion": {"inicio": None, "fin": None},
            "evaluacion": {"inicio": None, "fin": None},
            "postulacion": {"inicio": None, "fin": None}
        }
        self.orden_fases = ["inscripcion", "evaluacion", "postulacion"]
    def iniciar_sesion(self):#Iniciar sesión
        print(f"Bienvenido Administrador {self.nombre}")
    def cerrar_sesion(self):#Cerrar sesión
        print(f"Hasta luego Administrador {self.nombre}")
    def asignar_sede(self, sede):#Asignar sede
        print(f"Administrador {self.nombre} ha asignado la sede: {sede}")
    def cargar_datos(self):#Cargar datos
        print("El administrador está cargando datos...")
    def gestionar_soporte(self, solicitud):#Gestionar soporte
        print(f"Administrador {self.nombre} está gestionando la solicitud: {solicitud}")
    def _abrir_fase(self, fase, fecha_inicio, fecha_fin):#Abrir fase
        if fecha_inicio > fecha_fin:#Fecha inicio no puede ser mayor a fecha fin
            raise ValueError("La fecha inicio no puede ser mayor a la fecha fin")
        if self.fases[fase]["inicio"] is not None:#Validar si la fase ya está abierta
            raise ValueError(f"{fase.capitalize()} ya fue abierta")
        idx = self.orden_fases.index(fase)#Obtener índice de la fase
        if idx > 0:# Validar que la fase anterior esté cerrada
            fase_anterior = self.orden_fases[idx - 1]#Obtener fase anterior
            if self.fases[fase_anterior]["fin"] is None:#Validar si la fase anterior está cerrada
                raise ValueError(f"No se puede abrir {fase} antes de cerrar {fase_anterior}")
        self.fases[fase]["inicio"] = fecha_inicio#Abrir fase con fechas
        self.fases[fase]["fin"] = fecha_fin#Cerrar fase con fechas
        print(f"{fase.capitalize()} abierta desde {fecha_inicio} hasta {fecha_fin}")
    def _cerrar_fase(self, fase):#Cerrar fase
        if self.fases[fase]["inicio"] is None:#Validar si la fase está abierta
            print(f"No se puede cerrar {fase} que no se ha abierto")
            return
        self.fases[fase]["fin"] = date.today()#Cerrar fase con fecha actual
        print(f"{fase.capitalize()} cerrada")
    def _fase_activa(self, fase):#Verificar si fase está activa
        inicio = self.fases[fase]["inicio"]#Fecha inicio
        fin = self.fases[fase]["fin"]#Fecha fin
        if not inicio or not fin:#Si no hay fechas, fase no está activa
            return False
        hoy = date.today()#Fecha actual
        return inicio <= hoy <= fin#Verificar si la fase está activa
    def abrir_inscripciones(self, fecha_inicio, fecha_fin):#Abrir inscripciones
        self._abrir_fase("inscripcion", fecha_inicio, fecha_fin)
    def cerrar_inscripciones(self):#Cerrar inscripciones
        self._cerrar_fase("inscripcion")
    def inscripciones_activas(self):#Verificar si inscripciones están activas
        return self._fase_activa("inscripcion")
    def abrir_evaluaciones(self, fecha_inicio, fecha_fin):#Abrir evaluación
        self._abrir_fase("evaluacion", fecha_inicio, fecha_fin)
    def cerrar_evaluaciones(self):#Cerrar evaluación
        self._cerrar_fase("evaluacion")
    def evaluaciones_activas(self):#Verificar si evaluación está activa
        return self._fase_activa("evaluacion")
    def abrir_postulaciones(self, fecha_inicio, fecha_fin):#Abrir postulaciones
        self._abrir_fase("postulacion", fecha_inicio, fecha_fin)
    def cerrar_postulaciones(self):#Cerrar postulaciones
        self._cerrar_fase("postulacion")
    def postulaciones_activas(self):#Verificar si postulaciones están activas
        return self._fase_activa("postulacion")

class Aspirante(Usuario, Cargable, SolicitudAsistencia, GestorSede):#Clase Hija Aspirante de Usuario
    def __init__(self, cedula, nombre, apellido, correo, telefono, titulo, nota_grado):
        super().__init__(cedula, nombre, apellido, correo)
        self.telefono = telefono
        self.titulo = titulo
        self._nota_grado = None
        self.nota_grado = nota_grado
    @property#Propiedad nota grado
    def nota_grado(self):
        return self._nota_grado
    @nota_grado.setter#Setter nota grado con validación
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
    def crear_solicitud_asistencia(self, asunto):
        print(f"Aspirante {self.nombre} creó una solicitud sobre: {asunto}")
    def estado_solicitud(self, estado):
        print(f"Estado de solicitud: {estado}")
    def notificar_sede(self, sede):
        print(f"Aspirante {self.nombre} ha notificado la sede: {sede}")
    def imprimir_documentacion_sede(self, sede):
        print(f"Aspirante {self.nombre} imprime documentación para la sede: {sede}")

class Soporte(Usuario):#Clase Hija Soporte de Usuario
    def iniciar_sesion(self):
        print(f"Soporte {self.nombre} inició sesión.")
    def cerrar_sesion(self):
        print(f"Soporte {self.nombre} cerró sesión.")
    def recibir_asistencia(self, aspirante):
        print(f"Soporte atendiendo a {aspirante.nombre}")
    def derivar_asistencia(self, administrador):#Derivar asistencia
        print(f"Soporte deriva la asistencia al Administrador {administrador.nombre}")

class Profesor(Usuario):#Clase Hija Profesor de Usuario
    def __init__(self, cedula, nombre, apellido, correo, facultad):
        super().__init__(cedula, nombre, apellido, correo)
        self.facultad = facultad
    def iniciar_sesion(self):
        print(f"Profesor {self.nombre} inició sesión.")
    def cerrar_sesion(self):
        print(f"Profesor {self.nombre} cerró sesión.")
    def crear_cuestionario(self, tema, cantidad):
        print(f"Profesor {self.nombre} creó un cuestionario de '{tema}' con {cantidad} preguntas.")

class ManejadorAsistencia(ABC):#Clase abstracta ManejadorAsistencia
    def __init__(self, siguiente=None):
        self.siguiente = siguiente
    @abstractmethod#Método manejar solicitud
    def manejar(self, solicitud):
        pass

class SoporteHandler(ManejadorAsistencia):#Clase SoporteHandler
    def manejar(self, solicitud):#Manejar solicitud
        if solicitud == "tecnico":#Si es técnico
            print("Soporte resolvió el problema técnico")
        elif self.siguiente:#Si hay siguiente en la cadena
            print("Soporte escala al Administrador")
            self.siguiente.manejar(solicitud)

class AdministradorHandler(ManejadorAsistencia):#Clase AdministradorHandler
    def manejar(self, solicitud):#Manejar solicitud
        if solicitud in ["academico", "grave"]:#Si es académico o grave
            print("Administrador resolvió el problema")
        else:#Solicitud no válida
            print("Solicitud no válida")
