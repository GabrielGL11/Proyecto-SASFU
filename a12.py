import Usuario#Importar el módulo Usuario que contiene las clases necesarias
sistema = Usuario.SistemaFacade()#Crear una instancia del sistema
usuario_actual = None#Variable para almacenar el usuario que ha iniciado sesión
while True:#Menú principal
    print("\nBienvenido al sistema SASFU")
    print("1. Crear usuario")
    print("2. Iniciar sesión")
    print("3. Incripciones")
    print("4. Evaluaciones")
    print("5. Postulaciones")
    print("6. Reportes")
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
        exito = sistema.login(usuario, contrasena)#Intentar login
        if exito:#Si el login es exitoso
            aspirantes = sistema.repo.leer_todos()#Leer todos los aspirantes del repositorio
            aspirante_encontrado = None#Variable para almacenar el aspirante encontrado
            for a in aspirantes:#Buscar el aspirante con el usuario ingresado
                if a.get("usuario") == usuario:#Si se encuentra el aspirante
                    aspirante_encontrado = Usuario.Aspirante(
                        cedula=a.get("numero_identidad",""),#Número de identidad
                        nombre=a.get("nombres","SinNombre"),#Nombre del JSON
                        apellido=a.get("apellidos","SinApellido"),#Apellido del JSON
                        correo=a.get("correo",""),#Correo
                        telefono=a.get("celular",""),#Celular del JSON
                        titulo=a.get("titulo_bachiller_homologado",""),#Título
                        nota_grado=a.get("nota_grado",0)#Nota de grado
                    )
                    break
            if aspirante_encontrado:#Si se encontró el aspirante
                usuario_actual = aspirante_encontrado#Asignar el aspirante al usuario actual
                print(f"Bienvenido {usuario_actual.nombre}")
            else:#Si no se encontró el aspirante
                print("Usuario no encontrado como Aspirante.")
        else:#Login fallido
            print("Credenciales incorrectas.")
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
            if usuario_actual.inscripciones:
                for fac, car in usuario_actual.inscripciones.items():
                    print(f"Inscrito en: {fac} - {car}")#Mostrar inscripción
            else:#Si no hay inscripciones
                print("No tiene inscripciones registradas.")
        elif sub_opcion == "3":#Volver al menú principal
            continue
        else:#Opción inválida
            print("Opción inválida, intente nuevamente")
    elif opcion == "4":#Evaluaciones
        print("Función de evaluaciones aún no implementada")
    elif opcion == "5":#Postulaciones
        print("Función de postulaciones aún no implementada")
    elif opcion == "6":#Reportes
        print("Función de reportes aún no implementada")
    elif opcion == "7":#Salir
        print("Saliendo del sistema...")
        break
    else:#Opción inválida
        print("Opción inválida, intente nuevamente")
