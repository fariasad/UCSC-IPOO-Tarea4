from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Dict, List, Optional


class Persona:
    def __init__(self, rut: str, nombre: str, apellido_paterno: str, apellido_materno: str, correo: str):
        self._rut = rut
        self._nombre = nombre
        self._apellido_paterno = apellido_paterno
        self._apellido_materno = apellido_materno
        self._correo = correo

    @property
    def rut(self) -> str:
        return self._rut

    @property
    def nombre_completo(self) -> str:
        return f"{self._nombre} {self._apellido_paterno} {self._apellido_materno}"

    @property
    def correo(self) -> str:
        return self._correo

    def mostrar_resumen(self) -> str:
        return f"Persona: {self.nombre_completo} | RUT: {self._rut} | Correo: {self._correo}"


class Estudiante(Persona):
    def __init__(
        self,
        rut: str,
        nombre: str,
        apellido_paterno: str,
        apellido_materno: str,
        correo: str,
        carrera: str,
        estado_academico: str = "Activo",
    ):
        super().__init__(rut, nombre, apellido_paterno, apellido_materno, correo)
        self._carrera = carrera
        self._estado_academico = estado_academico
        self._inscripciones: List[Inscripcion] = []
        self._beca: Optional[Beca] = None

    @property
    def carrera(self) -> str:
        return self._carrera

    @property
    def estado_academico(self) -> str:
        return self._estado_academico

    @property
    def inscripciones(self) -> List[Inscripcion]:
        return list(self._inscripciones)

    @property
    def beca(self) -> Optional[Beca]:
        return self._beca

    def asignar_beca(self, beca: Beca) -> None:
        self._beca = beca

    def inscribir_en_seccion(self, seccion: SeccionAsignatura) -> str:
        inscripcion = Inscripcion(estudiante=self, seccion=seccion)
        seccion.agregar_inscripcion(inscripcion)
        self._inscripciones.append(inscripcion)
        return f"{self.nombre_completo} fue inscrito en la sección {seccion.codigo_seccion}."

    def calcular_promedio_general(self) -> float:
        notas = [ins.nota_final for ins in self._inscripciones if ins.nota_final is not None]
        if not notas:
            return 0.0
        return round(sum(notas) / len(notas), 2)

    # Polimorfismo: sobrescribe el método de Persona.
    def mostrar_resumen(self) -> str:
        return (
            f"Estudiante: {self.nombre_completo} | Carrera: {self._carrera} | "
            f"Estado: {self._estado_academico} | Promedio: {self.calcular_promedio_general()}"
        )


class Docente(Persona):
    def __init__(
        self,
        rut: str,
        nombre: str,
        apellido_paterno: str,
        apellido_materno: str,
        correo: str,
        especialidad: str,
    ):
        super().__init__(rut, nombre, apellido_paterno, apellido_materno, correo)
        self._especialidad = especialidad
        self._secciones_asignadas: List[SeccionAsignatura] = []

    @property
    def especialidad(self) -> str:
        return self._especialidad

    @property
    def secciones_asignadas(self) -> List[SeccionAsignatura]:
        return list(self._secciones_asignadas)

    def asignar_seccion(self, seccion: SeccionAsignatura) -> None:
        if seccion not in self._secciones_asignadas:
            self._secciones_asignadas.append(seccion)

    # Polimorfismo: sobrescribe el método de Persona.
    def mostrar_resumen(self) -> str:
        return (
            f"Docente: {self.nombre_completo} | Especialidad: {self._especialidad} | "
            f"Secciones asignadas: {len(self._secciones_asignadas)}"
        )


@dataclass
class Asignatura:
    codigo_asignatura: str
    nombre_asignatura: str
    creditos: int

    def descripcion(self) -> str:
        return f"{self.codigo_asignatura} - {self.nombre_asignatura} ({self.creditos} créditos)"


class SeccionAsignatura:
    """Representa una sección concreta de una asignatura."""

    def __init__(self, codigo_seccion: str, cupo_maximo: int, asignatura: Asignatura):
        self._codigo_seccion = codigo_seccion
        self._cupo_maximo = cupo_maximo
        self._asignatura = asignatura
        self._docente: Optional[Docente] = None
        self._inscripciones: List[Inscripcion] = []

    @property
    def codigo_seccion(self) -> str:
        return self._codigo_seccion

    @property
    def asignatura(self) -> Asignatura:
        return self._asignatura

    @property
    def docente(self) -> Optional[Docente]:
        return self._docente

    @property
    def inscripciones(self) -> List[Inscripcion]:
        return list(self._inscripciones)

    def asignar_docente(self, docente: Docente) -> str:
        self._docente = docente
        docente.asignar_seccion(self)
        return f"Docente {docente.nombre_completo} asignado a la sección {self._codigo_seccion}."

    def agregar_inscripcion(self, inscripcion: Inscripcion) -> None:
        self._inscripciones.append(inscripcion)

    def resumen(self) -> str:
        nombre_docente = self._docente.nombre_completo
        return (
            f"Sección: {self._codigo_seccion} | Asignatura: {self._asignatura.nombre_asignatura} | "
            f"Docente: {nombre_docente} | Inscritos: {len(self._inscripciones)}/{self._cupo_maximo}"
        )


class Inscripcion:
    def __init__(self, estudiante: Estudiante, seccion: SeccionAsignatura, fecha_inscripcion: Optional[date] = None):
        self._estudiante = estudiante
        self._seccion = seccion
        self._fecha_inscripcion = fecha_inscripcion or date.today()
        self._evaluaciones: Dict[str, float] = {}
        self._nota_final: Optional[float] = None
        self._estado_inscripcion = "Inscrito"

    @property
    def fecha_inscripcion(self) -> date:
        return self._fecha_inscripcion

    @property
    def nota_final(self) -> Optional[float]:
        return self._nota_final

    @property
    def estado_inscripcion(self) -> str:
        return self._estado_inscripcion

    def registrar_evaluacion(self, nombre_evaluacion: str, nota: float) -> None:
        self._evaluaciones[nombre_evaluacion] = nota

    def calcular_nota_final(self) -> float:
        if not self._evaluaciones:
            self._nota_final = 0.0
        else:
            self._nota_final = round(sum(self._evaluaciones.values()) / len(self._evaluaciones), 2)
        return self._nota_final

    def validar_aprobacion(self) -> str:
        nota = self.calcular_nota_final()
        self._estado_inscripcion = "Aprobado" if nota >= 4.0 else "Reprobado"
        return self._estado_inscripcion

    def resumen(self) -> str:
        nota = self._nota_final if self._nota_final is not None else "Sin calcular"
        return (
            f"Inscripción: {self._estudiante.nombre_completo} | "
            f"Sección: {self._seccion.codigo_seccion} | Nota final: {nota} | "
            f"Estado: {self._estado_inscripcion}"
        )


@dataclass
class Beca:
    nombre_beca: str
    porcentaje_descuento: float

    def calcular_descuento(self, monto_base: float) -> float:
        return round(monto_base * (self.porcentaje_descuento / 100), 0)


class PagoArancel:
    def __init__(self, estudiante: Estudiante, monto_base: float, fecha_vencimiento: date, beca: Optional[Beca] = None):
        self._estudiante = estudiante
        self._monto_base = monto_base
        self._fecha_vencimiento = fecha_vencimiento
        self._beca = beca
        self._pagado = False

    @property
    def pagado(self) -> bool:
        return self._pagado
    
    @property
    def monto_base(self) -> float:
        return self._monto_base

    @property
    def fecha_vencimiento(self) -> date:
        return self._fecha_vencimiento

    @property
    def beca(self) -> Optional[Beca]:
        return self._beca

    def calcular_monto_final(self) -> float:
        descuento = self._beca.calcular_descuento(self._monto_base) if self._beca else 0
        return max(0, self._monto_base - descuento)

    def registrar_pago(self) -> str:
        self._pagado = True
        return f"Pago registrado por ${self.calcular_monto_final():,.0f}."

    def estado_pago(self) -> str:
        return "Pagado" if self._pagado else f"Pendiente hasta {self._fecha_vencimiento.isoformat()}"

# Demostración por terminal.
def main() -> None:    
    docente = Docente(
        rut="12.298.229-7",
        nombre="Jose",
        apellido_paterno="Muñoz",
        apellido_materno="Rojas",
        correo="jose.muñoz@docentetarea4.cl",
        especialidad="Programación Orientada a Objetos",
    )

    estudiante1 = Estudiante(
        rut="22.222.222-2",
        nombre="Carlos",
        apellido_paterno="Gonzalez",
        apellido_materno="Soto",
        correo="carlos.gonzalez@alumnotarea4.cl",
        carrera="Ingeniería en Informática",
    )

    estudiante2 = Estudiante(
        rut="33.333.333-3",
        nombre="Antonio",
        apellido_paterno="Salas",
        apellido_materno="Fernandez",
        correo="antonio.salas@alumnotarea4.cl",
        carrera="Ingeniería en Informática",
    )

    asignatura = Asignatura("DSOO101", "Desarrollo de Sistemas Orientados a Objetos", 6)
    seccion = SeccionAsignatura("DSOO101-A", 30, asignatura)

    print("\n")
    print("\n===== COMIENZO DE LA APLICACIÓN ===========")
    print("\n===== ASIGNACION DE DOCENTE A SECCION =====")
    print(seccion.asignar_docente(docente))

    print("\n===== INSCRIPCIONES DE ESTUDIANTE EN SECCION =====")
    print(estudiante1.inscribir_en_seccion(seccion))
    print(estudiante2.inscribir_en_seccion(seccion))

    inscripcion1 = estudiante1.inscripciones[0]
    inscripcion1.registrar_evaluacion("Prueba 1", 5.0)
    inscripcion1.registrar_evaluacion("Prueba 2", 6.0)
    inscripcion1.registrar_evaluacion("Prueba 3", 7.0)
    inscripcion1.validar_aprobacion()

    inscripcion2 = estudiante2.inscripciones[0]
    inscripcion2.registrar_evaluacion("Prueba 1", 4.0)
    inscripcion2.registrar_evaluacion("Prueba 2", 5.0)
    inscripcion2.registrar_evaluacion("Prueba 3", 6.0)
    inscripcion2.validar_aprobacion()

    beca = Beca("Beca Excelencia Académica", 25)
    estudiante1.asignar_beca(beca)
    pago1 = PagoArancel(estudiante1, monto_base=1000000, fecha_vencimiento=date(2026, 5, 30), beca=beca)

    estudiante2.asignar_beca(None)  # Sin beca para el segundo estudiante
    pago2 = PagoArancel(estudiante2, monto_base=1000000, fecha_vencimiento=date(2026, 5, 30), beca=None)

    print("\n===== RESUMEN DE PERSONAS =====")
    personas: List[Persona] = [docente, estudiante1, estudiante2]

    for persona in personas:
        print(f"Tipo: {type(persona).__name__}")
        print(persona.mostrar_resumen())
        print("=" * 120)

    print("\n===== INFORMACIÓN ACADÉMICA =====")

    print("Asignatura:")
    print(asignatura.descripcion())

    print("\nSección:")
    print(seccion.resumen())

    print("\n===== DATOS ACADÉMICOS Y FINANCIEROS DE ESTUDIANTES =====")
    datos_estudiantes: List[tuple[Inscripcion, PagoArancel]] = [
        (inscripcion1, pago1),
        (inscripcion2, pago2),
    ]

    for indice, (ins, pago) in enumerate(datos_estudiantes, start=1):
        print(f"Estudiante {indice}:")
        print(ins.resumen())

        print("Información financiera:")
        print(f"Monto base: ${pago.monto_base:,.0f}")
        print(f"Fecha de vencimiento: {pago.fecha_vencimiento.isoformat()}")

        if pago.beca:
            print(f"Beca aplicada: {pago.beca.nombre_beca} ({pago.beca.porcentaje_descuento}%)")
        else:
            print("Sin beca aplicada")

        print(f"Monto final a pagar: ${pago.calcular_monto_final():,.0f}")
        print("Procesando pago...")
        print(pago.registrar_pago())
        print("Estado del pago: " + pago.estado_pago())
        print("=" * 120)

if __name__ == "__main__":
    main()
