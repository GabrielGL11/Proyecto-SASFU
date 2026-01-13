from abc import ABC#importar ABCMeta
from abc import abstractmethod#importar abstractmethod
import json#importar json
import os#importar os
from datetime import date, datetime, timedelta#importar date para manejo de fechas

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
    def estado_solicitud(self):
        pass

class GestorSede(ABC):#Clase GestorSede
    @abstractmethod#Método notificar sede
    def notificar_sede(self):
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
    
class RegistroInscripcion(ABC):
    def registrar_inscripcion(self, facultad: str, carrera: str):
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

class Repositorio(ABC):#Interfaz Repositorio
    @abstractmethod#Método leer datos
    def leer_todos(self):
        pass
    @abstractmethod#Método guardar datos
    def guardar_todos(self, datos):
        pass

class RepositorioAspirantesJSON(Repositorio):#Repositorio JSON
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

class RepositorioSolicitudesJSON(Repositorio):
    def __init__(self, archivo="solicitudes_asistencia.json"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.archivo = os.path.join(base_dir, archivo)
        if not os.path.exists(self.archivo):
            with open(self.archivo, "w", encoding="utf-8") as f:
                json.dump([], f)
    def leer_todos(self):#Leer base de datos
        with open(self.archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    def guardar_todos(self, datos):#Guardar base de datos
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

class ServicioAutenticacion:#Clase ServicioAutenticacion
    def __init__(self, repositorio: Repositorio):
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
    def __init__(self, repositorio: Repositorio):
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
    def asignar_sede(self, aspirante, sede, dia_hora=None):
        if not aspirante.inscripciones:
            print(f"No se puede asignar sede a {aspirante.nombre}: no tiene inscripción válida.")
            return
        if dia_hora is None:
            dia_hora = datetime.now().strftime("%Y-%m-%d %H:%M")  # Fecha y hora actual
        inicio_dt = datetime.strptime(dia_hora, "%Y-%m-%d %H:%M")        
        fecha_inicio_eval = inicio_dt.strftime("%Y-%m-%d %H:%M")
        fecha_fin_eval = (inicio_dt + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M")
        repo = RepositorioAspirantesJSON()
        aspirantes_db = repo.leer_todos()
        for a in aspirantes_db:
            if a["numero_identidad"] == aspirante.cedula_pasaporte:
                a["sede_asignada"] = {
                    "sede": sede,
                    "facultad": aspirante.inscripciones["facultad"],
                    "carrera": aspirante.inscripciones["carrera"],
                    "hora_dia": dia_hora,
                    "fecha_inicio_eval": fecha_inicio_eval,
                    "fecha_fin_eval": fecha_fin_eval
                }
                repo.guardar_todos(aspirantes_db)
                print(f"Administrador {self.nombre} ha asignado la sede {sede} a {aspirante.nombre}.")
                print(f"Horario: {dia_hora}, Evaluación de {fecha_inicio_eval} a {fecha_fin_eval}")
                return
        print("No se encontró al aspirante en la base de datos.")

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

class Aspirante(Usuario, Cargable, SolicitudAsistencia, GestorSede, RegistroInscripcion):#Clase Hija Aspirante de Usuario
    def __init__(self, cedula, nombre, apellido, correo, telefono, titulo, nota_grado):
        super().__init__(cedula, nombre, apellido, correo)
        self.telefono = telefono
        self.titulo = titulo
        self.nombre = nombre
        self._nota_grado = None
        self.nota_grado = nota_grado
        self.inscripciones = {}#Guardar inscripciones
        ruta_fac = os.path.join(os.path.dirname(__file__), "facultades_carreras.json")#Ruta archivo JSON real
        try:#Intentar cargar el archivo JSON
            with open(ruta_fac, "r", encoding="utf-8") as f:
                self.facultades_carreras = json.load(f)
        except Exception as e:#Si no existe, usar valor por defecto simplificado
            print("Error cargando facultades y carreras:", e)
            self.facultades_carreras = {
                "Ciencias de la Salud": ["Enfermería", "Fisioterapia", "Laboratorio Clínico", "Medicina", "Nutrición y Dietética", "Odontología", "Psicología", "Terapia Ocupacional"],
                "Ciencias Administrativas, Contables y Comercio": ["Administración De Empresas", "Auditoría y Control de Gestión", "Comercio Exterior", "Contabilidad Y Auditoría", "Gestión de Talento Humano", "Finanzas", "Gestión de la Información Gerencial", "Mercadotecnia o Marketing", "Gestión Pública y Desarrollo"],
                "Educación, Turismo y Humanidades": ["Educación Inicial", "Educación Básica", "Educación Básica Bilingüe", "Educación Inicial Bilingüe", "Educación Inclusiva", "Entrenamiento Deportivo", "Gestión Hotelera Internacional", "Pedagogía de la Lengua y la Literatura", "Pedagogía de los Idiomas Nacionales y Extranjeros", "Psicología Educativa", "Pedagogía de la Actividad Física y el Deporte", "Turismo Sostenible"],
                "Ingeniería, Industria y Arquitectura": ["Arquitectura", "Electricidad", "Ingeniería Civil", "Ingeniería Industrial", "Ingeniería Marítima"],
                "Ciencias de la Vida y Tecnologías": ["Agroindustria", "Agronegocios", "Agropecuaria", "Alimentos", "Biología", "Ingeniería Ambiental", "Software", "Tecnologías De La Información"],
                "Ciencias Sociales, Derecho y Bienestar": ["Comunicación", "Ciencias Políticas y Relaciones Internacionales", "Criminología y Ciencias Forenses", "Derecho", "Economía", "Trabajo Social"],
                "Artes": ["Arqueología", "Artes Escénicas", "Artes Plásticas", "Diseño Textil e Indumentaria", "Sociología"],
                "Formación Técnicas y Tecnológicas": ["Bienes Raíces", "Construcción Sismo Resistente", "Gastronomía", "Metalmecánica", "Comunicación para Televisión, Relaciones Públicas y Protocolo"]
            }
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
    def notificar_sede(self):
        repo = RepositorioAspirantesJSON()
        aspirantes = repo.leer_todos()
        for a in aspirantes:#Buscar aspirante por cédula
            if a["numero_identidad"] == self.cedula_pasaporte:#Encontrado aspirante
                sede_info = getattr(self, "sede_asignada", None)
                if sede_info:#Si hay sede asignada
                    print(f"Aspirante {self.nombre} notificado de su sede:")
                    print(f"  Sede: {sede_info['sede']}")
                    print(f"  Facultad: {sede_info['facultad']}")
                    print(f"  Carrera: {sede_info['carrera']}")
                    print(f"  Horario: {sede_info['hora_dia']}")
                    print(f"  Evaluación: del {sede_info['fecha_inicio_eval']} al {sede_info['fecha_fin_eval']}")
                else:#No tiene sede asignada
                    print(f"Aspirante {self.nombre} aún no tiene sede asignada.")
                return
        print(f"Aspirante {self.nombre} no se encontró en la base de datos.")
    def imprimir_documentacion_sede(self, sede):
        print(f"Aspirante {self.nombre} imprime documentación para la sede: {sede}")
    def registrar_inscripcion(self, facultad: str, carrera: str):#Registrar inscripción
        fac_lc = facultad.strip().lower()#Normalizar entrada
        car_lc = carrera.strip().lower()#Normalizar entrada
        for fac, carreras in self.facultades_carreras.items():#Buscar facultad
            if fac.lower() == fac_lc:#Facultad encontrada
                for c in carreras:#Buscar carrera
                    if c.lower() == car_lc:#Carrera encontrada
                        self.inscripciones = {"facultad": fac, "carrera": c}# Guardar inscripción
                        print(f"Aspirante {self.nombre} inscrito en {fac} - {c}")                        
                        repo = RepositorioAspirantesJSON()#Instancia del repositorio
                        aspirantes = repo.leer_todos()#Leer todos los aspirantes
                        for a in aspirantes:#Buscar aspirante por cédula
                            if a["numero_identidad"] == self.cedula_pasaporte:#Encontrado aspirante
                                a["inscripcion"] = self.inscripciones#Guardar inscripción
                                repo.guardar_todos(aspirantes)#Guardar datos
                                print("Inscripción guardada en la base de datos.")
                                return
                        print("No se encontró al aspirante en la base de datos.")
                        return
                print(f"No se encontró la carrera '{carrera}' en la facultad '{fac}'.")
                return
        print(f"No se encontró la facultad '{facultad}'.")
    def crear_solicitud_asistencia(self, asunto):#Crear solicitud de asistencia
        repo = RepositorioSolicitudesJSON()#Instancia del repositorio
        solicitudes = repo.leer_todos()#Leer todas las solicitudes
        nueva = {
            "id": len(solicitudes) + 1,
            "cedula_aspirante": self.cedula_pasaporte,
            "asunto": asunto,
            "estado": None,  # ← CLAVE
            "fecha": datetime.now().isoformat()
        }
        solicitudes.append(nueva)
        repo.guardar_todos(solicitudes)
        print(f"Aspirante {self.nombre} creó una solicitud de asistencia.")
    def estado_solicitud(self):
        repo = RepositorioSolicitudesJSON()
        solicitudes = repo.leer_todos()
        for s in solicitudes:
            if s["cedula_aspirante"] == self.cedula_pasaporte:
                print(f"Asunto: {s['asunto']} | Estado: {s['estado']}")
                return
        print("No tiene solicitudes registradas.")

class Soporte(Usuario):#Clase Hija Soporte de Usuario
    def iniciar_sesion(self):#Iniciar sesión
        print(f"Soporte {self.nombre} inició sesión.")
    def cerrar_sesion(self):#Cerrar sesión
        print(f"Soporte {self.nombre} cerró sesión.")
    def responder_solicitud(self, id_solicitud, aceptar: bool):#Responder solicitud
        repo = RepositorioSolicitudesJSON()#Instancia del repositorio
        solicitudes = repo.leer_todos()#Leer todas las solicitudes
        for s in solicitudes:#Buscar solicitud por ID
            if s["id"] == id_solicitud:#Solicitud encontrada
                if s["estado"] is not None:#Verificar si ya fue respondida
                    print("La solicitud ya fue respondida.")
                    return
                s["estado"] = aceptar#Actualizar estado
                repo.guardar_todos(solicitudes)#Guardar datos
                if aceptar:#Respuesta aceptada
                    print("Solicitud aceptada por Soporte.")
                else:#Respuesta rechazada
                    print("Solicitud rechazada por Soporte.")
                return
        print("Solicitud no encontrada.")

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
