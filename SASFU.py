'''Proyecto sobre el sistema de gestion de cupos universitarios'''
'''Sustainable application system for universities'''
'''SASFU'''
from abc import ABC#impotar ABCMeta
from abc import abstractmethod#importar abstractmethod
from Usuario import Aspirante

class Iniciar_fase(ABC):#Interfaz Iniciar_fase
    @abstractmethod
    def iniciar(self):
        pass

class Finalizar_fase(ABC):#Interfaz Finalizar_fase
    @abstractmethod
    def finalizar(self):
        pass

class Universidad(Iniciar_fase,Finalizar_fase):#Clase Universidad que hereda de Iniciar_fase y Finalizar_fase
    Pais = "Ecuador"
    def __init__(self, nombre:str, provincia:str, canton:str, direccion:str, enlace:str,universidad:str,tipo:str):
        self.nombre = nombre
        self.provincia = provincia
        self.canton = canton
        self.direccion = direccion
        self.enlace = enlace
        self.universidad = universidad
        self.tipo = tipo
    @property
    def universidad(self):#Getter universidad
        return self._universidad
    @universidad.setter
    def universidad(self, valor:str):#Setter universidad con validacion
        valor=valor.upper()
        valores_permitidos = ["PUBLICA", "PRIVADA"]
        if valor not in valores_permitidos:
            raise ValueError(f"El tipo de universidad debe ser uno de los siguientes: {valores_permitidos}.")             
        self._universidad = valor
    @property
    def tipo(self):#Getter tipo
        return self._tipo
    @tipo.setter
    def tipo(self, valor:str):#Setter tipo con validacion
        valor=valor.upper()
        valores_permitidos = ["NORMAL", "TECNICA"]
        if valor not in valores_permitidos:
            raise ValueError(f"El tipo de universidad publica debe ser uno de los siguientes: {valores_permitidos}.")             
        self._tipo = valor
    def iniciar(self):#Metodo iniciar la universidad
        print(f"La universidad {self.nombre} ha iniciado su admisión en {self.Pais}.")
    def finalizar(self):#Metodo finalizar la universidad
        print(f"La universidad {self.nombre} ha finalizado su admisión en {self.Pais}.")

class Oferta_Academica(Universidad):#Clase Oferta_Academica
    def __init__(self, carrera:str, cantidad:int, codigo:int, modalidad_oferta:str):
        self.carrera = carrera
        self.cantidad = cantidad
        self.codigo = codigo
        self.modalidad_oferta = modalidad_oferta
        self.cupos = cantidad
        self.postulantes = []
    @property
    def cantidad(self):#Getter cantidad
        return self._cantidad
    @cantidad.setter
    def cantidad(self, valor:int):#Setter cantidad con validacion
        if valor < 0:
            raise ValueError("La cantidad de cupos no puede ser negativa.")
        self._cantidad = valor  
    def crear_oferta(self):#Metodo crear_oferta
        print(f"La oferta académica para la carrera de {self.carrera} con {self.cantidad} cupos ha sido creada.")
    def esta_disponible(self): #Método esta_disponible
        return self.cantidad > 0
    def validar_modalidad(self): #Método validar_modalidad
        modalidades_validas = ["Presencial", "Virtual", "Híbrida"]
        if self.modalidad_oferta not in modalidades_validas:
            raise ValueError("Modalidad no válida")
    def validar_codigo(self): #Método validar_codigo
        if self.codigo <= 0:
            raise ValueError("El código debe ser un número positivo")
    def verificar_cupos(self): #Método verificar_cupos
        disponibles = self.cupos - len(self.postulantes)
        print(f"Cupos restantes para {self.carrera}: {disponibles}")
    
class Periodo(Iniciar_fase,Finalizar_fase):#Clase Periodo que hereda de Iniciar_fase y Finalizar_fase
    def __init__(self, Ano_Lectivo:str, Semestre:str):#Atributos de la clase Periodo
        self.Ano_Lectivo = Ano_Lectivo
        self.Semestre = Semestre
        print("Los datos del periodo fueron ingresados con éxitos")
    def iniciar(self):#Metodo iniciar el peridodo
        print(f"El periodo {self.Ano_Lectivo} - {self.Semestre} ha iniciado.")
    def finalizar(self):#Metodo finalizar el periodo
        print(f"El periodo {self.Ano_Lectivo} - {self.Semestre} ha finalizado.")

class Inscripcion(Iniciar_fase,Finalizar_fase):#Clase Inscripcion que hereda de Iniciar_fase y Finalizar_fase
    def __init__(self, carrera:str, facultad:str):
        self.carrera = carrera
        self.facultad = facultad
    def iniciar(self):#Metodo iniciar la inscripcion
        print(f"La inscripción para la carrera de {self.carrera} en la facultad de {self.facultad} ha iniciado.")
    def finalizar(self):#Metodo finalizar la inscripcion
        print(f"La inscripción para la carrera de {self.carrera} en la facultad de {self.facultad} ha finalizado.")
#inyeccion en proceso
#Clase_base
class tipo_de_examen(ABC):
    @abstractmethod
    def calcular_resultado(self, respuestas_correctas: int, total_preguntas: int) -> int:
        pass

    @abstractmethod
    def descripcion(self) -> str:
        pass

#Tipos de examen
class mixto(tipo_de_examen):
    def calcular_resultado(self, respuestas_correctas: int, total_preguntas: int) -> int:
        # ponderación 50% general + 50% area
        return int((respuestas_correctas / total_preguntas) * 1000)

    def descripcion(self):
        return "Examen mixto (conocimiento general y area conocimiento)"

class por_area(tipo_de_examen):
    def calcular_resultado(self, respuestas_correctas: int, total_preguntas: int) -> int:
        return int ((respuestas_correctas / total_preguntas) * 1000)

    def descripcion(self):
        return "Examen por área de conocimiento"
    
class general(tipo_de_examen):
    def calcular_resultado(self, respuestas_correctas: int, total_preguntas: int) -> int:
        return int((respuestas_correctas / total_preguntas) * 1000)
    
    def descripcion(self):
        return "Conocimiento general"

#inyección de dependencia
class Evaluacion:
    def __init__(self, tipo_examen: tipo_de_examen, horario: str, modalidad: str, sede: str):
        self.tipo_examen = tipo_examen  #dependencia
        self.horario = horario
        self.modalidad = modalidad
        self.sede = sede
        self._puntaje = 0

    def aplicar_examen(self, respuestas_correctas: int, total_preguntas: int):
        self._puntaje = self.tipo_examen.calcular_resultado(respuestas_correctas, total_preguntas)

    def mostrar_resultado(self):
        return (f"{self.tipo_examen.descripcion()} — "
                f"Puntaje obtenido: {self._puntaje}/1000 — "
                f"Modalidad: {self.modalidad}, Sede: {self.sede}")

class Postulacion(Iniciar_fase,Finalizar_fase,Aspirante):#Clase Postulacion que contiene los metodos iniciar y finalizar de las interfaces y hereda de Aspirante
    def __init__(self, carrera:str, nota_final:int):
        self.carrera = carrera
        self.nota_final = 0
        self.nota_final = nota_final
        
    @property    
    def nota_final(self):
        return self._nota_final


    @nota_final.setter
    def nota_final(self, valor : int):
        #Validacion de puntaje 
        if valor < 0 or valor > 1000:
            raise ValueError("La nota final debe estar entre 0 y 1000 puntos.")
        self._nota_final = valor
        
        
    def iniciar(self):#Metodo iniciar la postulación
        print(f"La postulacion para la carrera de {self.carrera} ha iniciado.")

    
    def finalizar(self):#Metodo finalizar la postulación
        print(f"La postulacion para la carrera de {self.carrera} ha finalizado.")


    def seleccionar_carrera(self):
        if self.nota_final >= 700:
            print(f"El aspirante ha sido **aceptado** en la carrera de {self.carrera} con {self.nota_final} puntos.")
        else:
            print(f"El aspirante **No alcanzo el puntaje minimo** para la carrera de {self.carrera} .")

class Servicio_web(Oferta_Academica):#Clase Servicio_web que hereda de Oferta_Academica
    Pais = "Ecuador"
    def __init__(self, provincia:str, enlace:str, carrera:str, cantidad:int):
        super().__init__(carrera, cantidad)
        self.nombre = provincia
        self.enlace = enlace 
        self.estado = "PENDIENTE"
    @property
    def estado(self):#Getter estado
        return self._estado
    @estado.setter
    def estado(self, valor:str):#Setter estado
        valor=valor.upper()
        valores_permitidos = ["PENDIENTE", "APROBADA", "RECHAZADA"]
        if valor not in valores_permitidos:
            raise ValueError(f"El estado debe ser uno de los siguientes: {valores_permitidos}.")             
        self._estado = valor
    def estado_servicio(self):#Metodo estado_servicio
        print(f"El servicio web de la provincia de {self.nombre} está activo.")
        if self.estado=="APROBADA":#Verifica si la oferta academica fue aceptada
            print("La oferta academica fue aceptada.")   
        elif self.estado=="RECHAZADA":#Verifica si la oferta academica fue rechazada
            print("La oferta academica fue rechazada.")
        else:#Verifica si la oferta academica esta pendiente
            print("La oferta academica está pendiente de revisión.")  
    
