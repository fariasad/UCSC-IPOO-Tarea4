# Sistema Académico Orientado a Objetos

## Descripción

Este proyecto corresponde al desarrollo de la Tarea 4, la cual consiste en el desarrollo de un sistema académico orientado a objetos, implementado en Python y diseñado previamente mediante UML con PlantUML. 

El sistema permite modelar y gestionar:
- Estudiantes y docentes
- Asignaturas y secciones
- Inscripciones y calificaciones
- Aprobación o reprobación
- Becas y pagos de arancel

---

## Tecnologías utilizadas

- Python 3
- PlantUML
- Visual Studio Code

---

## Estructura del proyecto

/Proyecto
├── Tarea4_Freddy_Arias_documento_proyecto.docx
├── Tarea4_Freddy_Arias_sistema_academico.py
├── Tarea4_Freddy_Arias_diagrama_sistema_academico.puml
├── README.md

---

## Clases principales

- Persona
- Estudiante
- Docente
- Asignatura
- SeccionAsignatura
- Inscripcion
- Beca
- PagoArancel

---

## Modelo del sistema

Los estudiantes y docentes se asignan a la sección (no a la asignatura).
La clase Inscripcion conecta Estudiante con SeccionAsignatura.

---

## Funcionalidades

- Inscribir estudiantes
- Registrar evaluaciones
- Calcular nota final
- Validar aprobación
- Aplicar becas
- Calcular arancel
- Registrar pagos

---

## Flujo

1. Crear objetos
2. Asignar docente
3. Inscribir estudiantes
4. Registrar notas
5. Calcular aprobación
6. Procesar pago

---

## Uso de listas y for

datos_estudiantes = [
    (inscripcion1, pago1),
    (inscripcion2, pago2)
]

for i, (ins, pago) in enumerate(datos_estudiantes, start=1):
    ...

---

## Ejecución

python sistema_academico.py

---

## Conclusión

El sistema cumple con los requerimientos de POO, demostrando encapsulamiento, herencia, polimorfismo y modularidad.
