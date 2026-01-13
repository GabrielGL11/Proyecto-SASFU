import Usuario#Importar el módulo Usuario que contiene las clases necesarias
sistema = Usuario.SistemaFacade()#Crear una instancia del sistema
usuario_actual = None#Variable para almacenar el usuario que ha iniciado sesión
while True: #Menú principal
    print("\nBienvenido al sistema SASFU")
    print("1. Crear usuario")
    print("2. Iniciar sesión")
    print("3. Incripciones")
    print("4. Evaluaciones")
    print("5. Postulaciones")
    print("6. Solicitudes de ayuda")
    print("7. Salir")
    opcion = input("Seleccione una opción (1-7): ")
    if opcion == "1":#Crear usuario
        cedula = input("Ingrese su cédula o pasaporte (será su usuario): ")
        contrasena = input("Ingrese su contraseña: ")
        confirmar = input("Confirme su contraseña: ")
        if contrasena != confirmar:#Verificar que las contraseñas coincidan
            print("Las contraseñas no coinciden")
            continue
        try:#Intentar registrar el usuario
            sistema.registrar_usuario(cedula, cedula, contrasena)
            print("Usuario creado correctamente.")#Mensaje de éxito
        except ValueError as e:#Capturar errores y mostrarlos
            print(f"Error: {e}")
    elif opcion == "2":#Iniciar sesión
        usuario = input("Ingrese su usuario (cédula): ")
        contrasena = input("Ingrese su contraseña: ")
        aspirantes = sistema.repo.leer_todos()#Lista de aspirantes
        aspirante_encontrado = None#Inicializar variable para el aspirante encontrado
        for a in aspirantes:#Buscar el aspirante en la base de datos
            if a.get("numero_identidad") == usuario:#Coincidencia de cédula
                aspirante_encontrado = Usuario.Aspirante(
                    cedula=a.get("numero_identidad", ""),
                    nombre=a.get("nombres", "SinNombre"),
                    apellido=a.get("apellidos", "SinApellido"),
                    correo=a.get("correo", ""),
                    telefono=a.get("celular", ""),
                    titulo=a.get("titulo_bachiller_homologado", ""),
                    nota_grado=a.get("nota_grado", 0)
                )
                aspirante_encontrado.inscripciones = a.get("inscripcion", {})#Cargar inscripciones
                aspirante_encontrado.sede_asignada = a.get("sede_asignada", {})#Cargar sede asignada
                aspirante_encontrado.contrasena = a.get("contrasena", "")#Cargar contraseña
                break
        if aspirante_encontrado and contrasena == aspirante_encontrado.contrasena:#Verificar credenciales
            usuario_actual = aspirante_encontrado#Asignar el usuario actual
            print(f"Bienvenido {usuario_actual.nombre}")#Mensaje de bienvenida
        else:#Credenciales incorrectas
            print("Usuario o contraseña incorrectos")
    elif opcion == "3":#Inscripciones
        if usuario_actual is None:#Verificar si el usuario ha iniciado sesión
            print("Debe iniciar sesión primero.")
            continue
        print("=== Menú Inscripciones ===")
        print("1. Realizar inscripción")
        print("2. Ver estado de inscripción")
        print("3. Volver al menú principal")
        sub_opcion = input("Seleccione una opción (1-3): ")
        if sub_opcion == "1":#Realizar inscripción
            facultad = input("Ingrese la facultad: ")
            carrera = input("Ingrese la carrera: ")
            usuario_actual.registrar_inscripcion(facultad, carrera)#Registrar inscripción
        elif sub_opcion == "2":#Ver estado de inscripción
            if usuario_actual.inscripciones:#Verificar si hay inscripciones
                for fac, car in usuario_actual.inscripciones.items():
                    print(f"Inscrito en: {fac} - {car}")#Mostrar inscripción
            else:  # Si no hay inscripciones
                print("No tiene inscripciones registradas.")
        elif sub_opcion == "3":#Volver al menú principal
            continue
        else:#Opción inválida
            print("Opción inválida, intente nuevamente")
    elif opcion == "4":#Evaluaciones
        if usuario_actual is None:#Verificar si el usuario ha iniciado sesión
            print("Debe iniciar sesión primero.")
            continue
        print("=== Menú Evaluaciones ===")
        print("1. Ver sede y horario de evaluación")
        print("2. Ver nota de evaluación")
        print("3. Volver al menú principal")
        sub_opcion = input("Seleccione una opción (1-3): ")
        if sub_opcion == "1":#Mostrar sede y horario de evaluación
            if usuario_actual.inscripciones:#Verificar si hay inscripciones
                usuario_actual.notificar_sede()#Notificar sede
            else:#Si no hay inscripciones
                print("No tiene inscripción registrada. No puede ver sede ni evaluación.")
        elif sub_opcion == "2":#Mostrar nota de evaluación
            print("Función de nota de evaluación aún no implementada")
        elif sub_opcion == "3":#Volver al menú principal
            continue
        else:
            print("Opción inválida, intente nuevamente")
    elif opcion == "5":#Postulaciones
        print("Función de postulaciones aún no implementada")
    elif opcion == "6":#Solicitudes de ayuda
        if usuario_actual is None:#Verificar si el usuario ha iniciado sesión
            print("Debe iniciar sesión primero.")
            continue
        mensaje = input("Describa su problema o solicitud: ")
        from Usuario import RepositorioSolicitudesJSON#Importar el repositorio de solicitudes
        repo = RepositorioSolicitudesJSON()#Crear instancia del repositorio
        solicitudes = repo.leer_todos()#Leer todas las solicitudes
        nueva_solicitud = {
            "id": len(solicitudes) + 1,
            "cedula_aspirante": usuario_actual.cedula_pasaporte,
            "mensaje": mensaje,
            "estado": None#Estado PENDIENTE
        }
        solicitudes.append(nueva_solicitud)#Agregar nueva solicitud
        repo.guardar_todos(solicitudes)#Guardar todas las solicitudes
        print("Solicitud enviada correctamente. Queda en estado PENDIENTE.")
    elif opcion == "7":#Salir
        print("Saliendo del sistema...")
        break
    else:#Opción inválida
        print("Opción inválida, intente nuevamente")
        