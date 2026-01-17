import Usuario#Importar módulo Usuario
from datetime import date#Importar date para manejo de fechas y abajo crea la cuenta de administrador
from SASFU import Inscripcion, Postulacion, ObservadorAdmin, ObservadorAspirante#Importar módulos de SASFU
from GeneradorBDHorarioEvaluacion import crear_base_datos_horarios
admin = Usuario.Administrador("10101010", "Chris", "ADMIN", "admin@hotmail.com", "Administrador")
repo = Usuario.RepositorioAspirantesJSON()#Repositorio de aspirantes
repo_solicitudes = Usuario.RepositorioSolicitudesJSON()#Repositorio de solicitudes
admin.iniciar_sesion()
while True:#Menú de administrador
    print("\n=== Menú de Administrador SASFU ===")
    print("1. Abrir inscripciones")
    print("2. Cerrar inscripciones")
    print("3. Abrir evaluaciones")
    print("4. Generar base de datos de horarios (JSON)")
    print("5. Asignar evaluaciones a aspirantes")
    print("6. Cerrar evaluaciones")
    print("7. Abrir postulaciones")
    print("8. Cerrar postulaciones")
    print("9. Gestionar solicitudes derivadas por soporte")
    print("10. Salir")
    opcion = input("Seleccione una opción (1-10): ")
    if opcion == "1":#Abrir inscripciones
        print("=== Abrir Inscripciones ===")
        fi = input("Fecha inicio (YYYY-MM-DD): ")
        ff = input("Fecha fin (YYYY-MM-DD): ")
        try:#Validar formato de fechas
            fecha_inicio = date.fromisoformat(fi)#Convertir a objeto date
            fecha_fin = date.fromisoformat(ff)#Convertir a objeto date
            admin.abrir_inscripciones(fecha_inicio, fecha_fin)#Abrir inscripciones
            ins = Inscripcion("", "")#Crear instancia de Inscripcion
            ins.agregar_observador(ObservadorAdmin())#Agregar observador admin
            ins.agregar_observador(ObservadorAspirante())#Agregar observador aspirante
            ins.iniciar()#Iniciar inscripciones
        except ValueError as e:#Capturar error en formato de fechas
            print("Error en las fechas:", e)
    elif opcion == "2":#Cerrar inscripciones
        admin.cerrar_inscripciones()#Cerrar inscripciones
        ins = Inscripcion("", "")#Crear instancia de Inscripcion
        ins.agregar_observador(ObservadorAdmin())#Agregar observador admin
        ins.agregar_observador(ObservadorAspirante())#Agregar observador aspirante
        ins.finalizar()#Finalizar inscripciones
    elif opcion == "3":#Abrir evaluaciones
        print("=== Abrir Evaluaciones ===")
        fi = input("Fecha inicio (YYYY-MM-DD): ")
        ff = input("Fecha fin (YYYY-MM-DD): ")
        try:#Validar formato de fechas
            fecha_inicio = date.fromisoformat(fi)
            fecha_fin = date.fromisoformat(ff)
            admin.abrir_evaluaciones(fecha_inicio, fecha_fin)#Abrir evaluaciones
        except ValueError as e:#Capturar error en formato de fechas
            print("Error en las fechas:", e)
    elif opcion == "4":#Generar la base de datos para los horarios
        confirmar = input("¿Desea generar/reemplazar la base de datos de horarios? (s/n): ").lower()
        if confirmar == "s":#Genera la base de datos de los horarios
            total = crear_base_datos_horarios()
            print(f"Base de datos creada correctamente")
            print(f"Total de registros: {total}")
        else:#No genera la base de datos
            print("Operación cancelada")
    elif opcion == "5":#Asignar evaluaciones a aspirantes
        print("=== Asignar Sede a Aspirante ===")
        cedula = input("Ingrese la cédula del aspirante: ")#Pedir cédula
        aspirantes_db = repo.leer_todos()#Leer aspirantes
        aspirante_encontrado = None
        for a in aspirantes_db:#Buscar aspirante por cédula
            if a.get("numero_identidad", "").strip() == cedula.strip():
                aspirante_encontrado = Usuario.Aspirante(
                    cedula=a.get("numero_identidad", ""),
                    nombre=a.get("nombres", "SinNombre"),
                    apellido=a.get("apellidos", "SinApellido"),
                    correo=a.get("correo", ""),
                    telefono=a.get("celular", ""),
                    titulo=a.get("titulo_bachiller_homologado", ""),
                    nota_grado=a.get("nota_grado", 0)
                )
                aspirante_encontrado.inscripciones = a.get("inscripcion", {})
                break
        if aspirante_encontrado is None:#Validar que exista el aspirante
            print("No se encontró al aspirante con esa cédula.")
            continue
        if not aspirante_encontrado.inscripciones:#Validar que tenga inscripción
            print("El aspirante no tiene inscripción registrada.")
            continue
        codigo_sala = int(input("Ingrese el código de la sala: "))#Pedir solo el código de la sala
        fecha = input("Ingrese la fecha de evaluación (YYYY-MM-DD): ")#Pedir fecha de evaluación
        admin.asignar_sede(aspirante_encontrado, codigo_sala, fecha)#Asignar sede
    elif opcion == "6":#Cerrar evaluaciones
        admin.cerrar_evaluaciones()
    elif opcion == "7":#Abrir postulaciones
        print("=== Abrir Postulaciones ===")
        fi = input("Fecha inicio (YYYY-MM-DD): ")
        ff = input("Fecha fin (YYYY-MM-DD): ")
        try:#Validar formato de fechas
            fecha_inicio = date.fromisoformat(fi)#Convertir a objeto date
            fecha_fin = date.fromisoformat(ff)#Convertir a objeto date
            admin.abrir_postulaciones(fecha_inicio, fecha_fin)#Abrir postulaciones
        except ValueError as e:#Capturar error en formato de fechas
            print("Error en las fechas:", e)
    elif opcion == "8":#Cerrar postulaciones
        admin.cerrar_postulaciones()#Cerrar postulaciones
        post = Postulacion("", 0)#Crear instancia de Postulacion
        post.agregar_observador(ObservadorAdmin())#Agregar observador admin
        post.agregar_observador(ObservadorAspirante())#Agregar observador aspirante
        post.finalizar()#Finalizar postulaciones
    elif opcion == "9":#Gestionar solicitudes derivadas por soporte
        solicitudes = repo_solicitudes.leer_todos()#Leer todas las solicitudes
        solicitudes_derivadas = [
            s for s in solicitudes if s.get("tipo") in ["tecnico", "academico", "grave"] and s.get("estado") is True
        ]
        if not solicitudes_derivadas:#Verificar si hay solicitudes derivadas
            print("No hay solicitudes derivadas para gestionar.")
            continue
        print("\n--- SOLICITUDES DERIVADAS ---")
        for s in solicitudes_derivadas:#Mostrar solicitudes derivadas
            print(f"ID: {s['id']}")
            print(f"Cédula Aspirante: {s['cedula_aspirante']}")
            print(f"Asunto: {s.get('asunto', s.get('mensaje',''))}")
            print(f"Tipo: {s['tipo']}")
            print("-" * 30)
        id_solicitud = int(input("Ingrese el ID de la solicitud para actualizar (o 0 para salir): "))
        if id_solicitud != 0:#Actualizar estado de solicitud derivada
            solicitud = next((x for x in solicitudes_derivadas if x["id"] == id_solicitud), None)
            if solicitud:#Si se encuentra la solicitud
                decision = input("¿Aceptar la solicitud? (s/n): ").lower()
                if decision == "s":#Aceptar solicitud
                    solicitud["estado"] = True
                elif decision == "n":#Rechazar solicitud
                    solicitud["estado"] = False
                else:#Opción inválida
                    print("Opción inválida")
                repo_solicitudes.guardar_todos(solicitudes)
                print(f"Solicitud ID {id_solicitud} actualizada.")
            else:#No se encontró la solicitud con ese ID
                print("No se encontró la solicitud con ese ID.")
    elif opcion == "10":#Salir del menú
        print("Saliendo del menú de administrador...")
        admin.cerrar_sesion()
        break
    else:#Opción inválida
        print("Opción inválida, intente nuevamente")
        