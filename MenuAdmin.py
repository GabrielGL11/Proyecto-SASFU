import Usuario#Importar módulo Usuario
from datetime import date#Importar date para manejo de fechas y abajo crea la cuenta de administrador
admin = Usuario.Administrador("01010101", "David", "ULEAMBUENASMANOS", "admin@hotmail.com", "Administrador")
while True:#Menú de administrador
    print("\nMenú de Administrador SASFU")
    admin.iniciar_sesion()
    print("1. Abrir inscripciones")
    print("2. Cerrar inscripciones")
    print("3. Abrir evaluaciones")
    print("4. Asignar evaluaciones a aspirantes")
    print("5. Cerrar evaluaciones")
    print("6. Abrir postulaciones")
    print("7. Cerrar postulaciones")
    print("8. Salir")
    opcion = input("Seleccione una opción (1-8): ")#Solicitar opción
    if opcion == "1":#Abrir inscripciones con fechas personalizadas
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
    elif opcion == "3":#Abrir evaluaciones con fechas personalizadas
        print("=== Abrir Evaluaciones ===")
        fi = input("Fecha inicio (YYYY-MM-DD): ")
        ff = input("Fecha fin (YYYY-MM-DD): ")
        try:#Validar formato de fechas
            fecha_inicio = date.fromisoformat(fi)
            fecha_fin = date.fromisoformat(ff)
            admin.abrir_evaluaciones(fecha_inicio, fecha_fin)
        except ValueError as e:
            print("Error en las fechas:", e)
    elif opcion == "4":#Asignar evaluaciones a aspirantes
        print("=== Asignar Sede a Aspirante ===")
        cedula = input("Ingrese la cédula del aspirante: ")
        repo = Usuario.RepositorioAspirantesJSON()
        aspirantes_db = repo.leer_todos()
        aspirante_encontrado = None
        for a in aspirantes_db:#Buscar aspirante por cédula
            if a.get("numero_identidad", "").strip() == cedula.strip():
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
        sede = input("Ingrese la sede a asignar: ")#Solicitar sede
        dia_hora = input("Ingrese día y hora de evaluación (YYYY-MM-DD HH:MM) o deje vacío para usar fecha actual: ")
        if not dia_hora.strip():#Si no se ingresa fecha y hora
            dia_hora = None  
        admin.asignar_sede(aspirante_encontrado, sede, dia_hora)#Asignar sede
    elif opcion == "4":#Cerrar evaluaciones
        admin.cerrar_evaluaciones()
    elif opcion == "5":#Abrir postulaciones con fechas personalizadas
        print("=== Abrir Postulaciones ===")
        fi = input("Fecha inicio (YYYY-MM-DD): ")
        ff = input("Fecha fin (YYYY-MM-DD): ")
        try:#Validar formato de fechas
            fecha_inicio = date.fromisoformat(fi)
            fecha_fin = date.fromisoformat(ff)
            admin.abrir_postulaciones(fecha_inicio, fecha_fin)
        except ValueError as e:
            print("Error en las fechas:", e)
    elif opcion == "7":#Cerrar postulaciones
        admin.cerrar_postulaciones()
    elif opcion == "8":#Salir del menú
        print("Saliendo del menú de administrador...")
        admin.cerrar_sesion()
        break
    else:#Opción inválida
        print("Opción inválida, intente nuevamente")
        