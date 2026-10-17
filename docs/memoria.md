# Memoria y aprendizaje de Pantera Negra

## Clasificación

| Destino | Contenido |
| --- | --- |
| Proyecto destino | Arquitectura, negocio, convenciones, comandos, restricciones y errores propios |
| Vengadores | Mejoras reutilizables de delegación, contexto, revisión y coordinación |
| Registro de tarea | Logs, hipótesis descartadas, reproducciones y detalles temporales |

Pantera analiza informes de Viuda, Hulk y Guardianes, además del resultado de deploy.
Propone ajustes antes de la entrega y los consolida con evidencia final. Puede
descartar una propuesta si las comprobaciones posteriores la contradicen.

## Formato de regla

Cada regla registra: ID, destino, disparador, acción, verificación, alcance,
evidencia (tarea/commit/artefacto), estado y versión. Estados: propuesta, vigente,
reemplazada o retirada. La política del destino determina quién valida los cambios;
una propuesta no se carga como instrucción vigente.

Antes de agregar, buscar duplicados, contradicciones y reglas obsoletas. Actualizar
o consolidar antes de expandir. Una regla global debe justificar su reutilización
y conservar condiciones de aplicación; no generalizar desde un fallo aislado.
Nunca incluir secretos o información privada de un destino en Vengadores.

## Resumen de memory.md y selección de contexto

Ant-Man localiza las fuentes de memoria y reglas según la configuración del
proyecto; no presupone una ruta universal de Codex. Conserva los originales y
prepara un resumen operativo con referencias a secciones, hashes y revisión analizada.
Cambios en fuentes invalidan el resumen. Jarvis solo pasa ese paquete a los agentes
que lo necesitan; no lo redacta ni interpreta.

El resumen incluye arquitectura, criterios de programación, comandos, restricciones
y aprendizajes vigentes. Las contradicciones se registran para resolverlas, no se
eliminan silenciosamente al resumir. Las reglas compartidas no desplazan las
instrucciones del usuario ni las reglas específicas aplicables al destino.

Ant-Man selecciona, según la configuración y la tarea, el contexto pertinente para
cada rol y devuelve referencias a los artefactos extensos. Jarvis entrega ese paquete
sin alterarlo y registra qué referencias recibió cada agente. Reducir tokens no debe
omitir requisitos o riesgos relevantes para la tarea.

## Evaluación

Comparar consumo de tokens, errores repetidos, ciclos de corrección y cumplimiento
de criterios en tareas comparables. Mantener evidencia antes/después y distinguir
beneficio esperado de observado. Versionar o revertir cambios de memoria que aumenten
errores o creen conflictos. Ninguna mejora se declara validada solo por reducir tokens.

