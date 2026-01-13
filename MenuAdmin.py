import Usuario#Importar módulo Usuario
from datetime import date#Importar date para manejo de fechas y abajo crea la cuenta de administrador
admin = Usuario.Administrador("01010101", "David", "ULEAMBUENASMANOS", "admin@hotmail.com", "Administrador")
repo = Usuario.RepositorioAspirantesJSON()#Repositorio de aspirantes
repo_solicitudes = Usuario.RepositorioSolicitudesJSON()#Repositorio de solicitudes
while True:#Menú de administrador
    print("\n=== Menú de Administrador SASFU ===")
    admin.iniciar_sesion()
    print("1. Abrir inscripciones")
    print("2. Cerrar inscripciones")
    print("3. Abrir evaluaciones")
    print("4. Asignar evaluaciones a aspirantes")
    print("5. Cerrar evaluaciones")
    print("6. Abrir postulaciones")
    print("7. Cerrar postulaciones")
    print("8. Gestioionar solicitudes derivadas por soporte")
    print("9. Salir")
    opcion = input("Seleccione una opción (1-9): ")
    if opcion == "1":#Abrir inscripciones
        print("=== Abrir Inscripciones ===")
        fi = input("Fecha inicio (YYYY-MM-DD): ")
        ff = input("Fecha fin (YYYY-MM-DD): ")
        try:#Validar formato de fechas
            fecha_inicio = date.fromisoformat(fi)
            fecha_fin = date.fromisoformat(ff)
            admin.abrir_inscripciones(fecha_inicio, fecha_fin)
        except ValueError as e:#Capturar error en formato de fechas
            print("Error en las fechas:", e)
    elif opcion == "2":#Cerrar inscripciones
        admin.cerrar_inscripciones()
    elif opcion == "3":#Abrir evaluaciones
        print("=== Abrir Evaluaciones ===")
        fi = input("Fecha inicio (YYYY-MM-DD): ")
        ff = input("Fecha fin (YYYY-MM-DD): ")
        try:#Validar formato de fechas
            fecha_inicio = date.fromisoformat(fi)
            fecha_fin = date.fromisoformat(ff)
            admin.abrir_evaluaciones(fecha_inicio, fecha_fin)
        except ValueError as e:#Capturar error en formato de fechas
            print("Error en las fechas:", e)
    elif opcion == "4":#Asignar evaluaciones a aspirantes
        print("=== Asignar Sede a Aspirante ===")
        cedula = input("Ingrese la cédula del aspirante: ")
        aspirantes_db = repo.leer_todos()#Leer todos los aspirantes
        aspirante_encontrado = None#Buscar aspirante por cédula
        for a in aspirantes_db:#Buscar aspirante por cédula
            if a.get("numero_identidad","").strip() == cedula.strip():#Coincidencia de cédula
                aspirante_encontrado = Usuario.Aspirante(
                    cedula=a.get("numero_identidad",""),
                    nombre=a.get("nombres","SinNombre"),
                    apellido=a.get("apellidos","SinApellido"),
                    correo=a.get("correo",""),
                    telefono=a.get("celular",""),
                    titulo=a.get("titulo_bachiller_homologado",""),
                    nota_grado=a.get("nota_grado",0)
                )
                aspirante_encontrado.inscripciones = a.get("inscripcion", {})
                break
        if aspirante_encontrado is None:#Si no se encuentra el aspirante
            print("No se encontró al aspirante con esa cédula.")
            continue
        if not aspirante_encontrado.inscripciones:#Verificar si el aspirante tiene inscripción válida
            print("El aspirante no tiene inscripción válida. No se puede asignar sede.")
            continue
        sede = input("Ingrese la sede a asignar: ")
        dia_hora = input("Ingrese día y hora de evaluación (YYYY-MM-DD HH:MM) o deje vacío para usar fecha actual: ")
        if not dia_hora.strip():#Si no se ingresa fecha y hora
            dia_hora = None
        admin.asignar_sede(aspirante_encontrado, sede, dia_hora)
    elif opcion == "5":#Cerrar evaluaciones
        admin.cerrar_evaluaciones()
    elif opcion == "6":#Abrir postulaciones
        print("=== Abrir Postulaciones ===")
        fi = input("Fecha inicio (YYYY-MM-DD): ")
        ff = input("Fecha fin (YYYY-MM-DD): ")
        try:#Validar formato de fechas
            fecha_inicio = date.fromisoformat(fi)
            fecha_fin = date.fromisoformat(ff)
            admin.abrir_postulaciones(fecha_inicio, fecha_fin)
        except ValueError as e:#Capturar error en formato de fechas
            print("Error en las fechas:", e)
    elif opcion == "7":#Cerrar postulaciones
        admin.cerrar_postulaciones()
    elif opcion == "8":#Gestionar solicitudes derivadas por soporte
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
    elif opcion == "9":#Salir del menú
        print("Saliendo del menú de administrador...")
        admin.cerrar_sesion()
        break
    else:#Opción inválida
        print("Opción inválida, intente nuevamente")
