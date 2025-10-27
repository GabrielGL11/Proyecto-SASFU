import SASFU
aspirante1 = SASFU.Aspirante("1312685560", "Juan", "Pérez", "juan@gmail.com", "099000933", True, 8.02)
soport1 = SASFU.Soporte("0923456789", "María", "Gómez", "maria@soporte.com", "098765432")
profesor1 = SASFU.Profesor("1002003004","Carlos","Lopez","carlez@hotmail.com", "arquitecto")
aspirante2=SASFU.Aspirante("1312685560","Daniel","Correa","Daniel@gmail.com","097859433",True,8.02)
aspirante2.cargar_datos()
aspirante2.iniciar_sesion()
print(aspirante2.nacionalidad())
aspirante2.cerrar_sesion()
profesor1.crear_cuestionario("Matemáticas", 10)

aspirante1.iniciar_sesion()
soport1.iniciar_sesion()

soport1.recibir_asistencia(aspirante1)

hora = input("hora del examen:")
modalidad = input("presencial o virtual:")
sede = input("sede:")

evaluacion1 = SASFU.Evaluacion(SASFU.mixto(), hora, modalidad, sede)
evaluacion1.aplicar_examen(respuestas_correctas=45, total_preguntas=50)

print(evaluacion1.mostrar_resultado())
