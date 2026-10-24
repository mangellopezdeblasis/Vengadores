# Flujo de Jarvis

Para crear o ajustar skills y subagentes, Jarvis delega directamente a Nick Fury.
La autoría no inicia automáticamente el flujo de producto o deploy.

## Estados y avance

| Estado | Responsable | Entregable / condición para avanzar |
| --- | --- | --- |
| Preparación | Jarvis | ID, repositorio, referencias de versión, configuración y límites; bloquea si falta el skill de delegación |
| Contexto inicial | Ant-Man | Paquete de reglas/memoria, versiones, recursos y restricciones para los agentes |
| Investigación | Ant-Man y Spider-Man en paralelo | Ant-Man entrega mapa de impacto y versión del grafo; Spider-Man diagnostica con el contexto inicial y refina con el mapa cuando esté disponible |
| Especificación | Capitán América ↔ Spider-Man | Criterios verificables y decisiones resueltas, usando el paquete de contexto de Ant-Man |
| Planificación | Vision | Plan técnico: tareas, dependencias, contratos y verificaciones; recomienda paralelismo |
| Implementación | Uno o varios Thor | Cambios por tarea en ramas y worktrees propios |
| Integración candidata | Thor, con rol de integrador delegado por Jarvis | Cambios reunidos, conflictos resueltos, verificaciones básicas y SHA de la candidata |
| Revisión | Viuda Negra y Hulk en paralelo | Conformidad con especificación/plan y hallazgos adversariales |
| E2E candidata | Guardianes de la Galaxia | Recorridos de aceptación y regresiones de Hulk ejecutados sobre la candidata |
| Aprendizaje propuesto | Pantera Negra | Ajustes de reglas clasificados por destino, con evidencia |
| Integración y deploy | Soldado del Invierno | Merge a dev y despliegue del commit integrado |
| E2E del despliegue en dev | Guardianes de la Galaxia | Recorridos de aceptación y regresiones ejecutados contra el SHA desplegado |
| Cierre de tarea | Pantera Negra; Jarvis registra el estado | Conocimiento validado/versionado; Jarvis entrega al usuario estados y referencias de informes |

Jarvis solo invoca el skill de delegación, pasa entradas y referencias, agenda las
llamadas según las dependencias y registra estados. No produce análisis, código ni
veredictos técnicos. Ant-Man prepara el paquete de contexto con fuentes y hashes;
los especialistas entregan evaluaciones y síntesis. Los agentes no necesitan
compartir el historial completo.

## Paralelismo y worktrees

- Vision evalúa independencia y recomienda unidades paralelas con contratos compartidos.
  Jarvis decide el agendado según esa evidencia, las dependencias y límites.
- Cada Thor tiene rama y worktree propios, derivados de un commit base identificado.
- Cada sandbox cloud puede tener su propio clon y crear allí su worktree.
- Un worktree no aísla procesos, red ni credenciales: la ejecución requiere sandboxes.
- Vision propone propiedad de archivos y recursos en el plan técnico; Jarvis decide
  agendar o serializar llamadas, respetando restricciones y sin editar worktrees.
- La revisión conjunta ocurre sobre la rama candidata, no solo sobre cambios individuales.
- Al cambiar el commit revisado se invalidan los controles afectados. Antes del merge,
  comprobar que los resultados corresponden al candidato final y a la base dev actual.

## Correcciones y bloqueos

Jarvis delega cada hallazgo al responsable indicado por la revisión especializada:

| Causa | Retorno |
| --- | --- |
| Contexto o impacto incorrectos | Ant-Man |
| Diagnóstico sin evidencia suficiente | Spider-Man |
| Ambigüedad de comportamiento | Capitán América ↔ Spider-Man |
| Plan incompleto o dependencia omitida | Vision |
| Implementación defectuosa | Thor |
| Decisión de producto ausente | Responsable humano de la tarea |

Después de una corrección se repiten las verificaciones afectadas. Jarvis controla
el contador de llamadas y los límites configurados; al alcanzarlos registra un
bloqueo y lo comunica con referencias. Solo registra controles como aprobados cuando
el agente responsable entrega estado, SHA y evidencia. No juzga por sí mismo la
calidad técnica de esa evidencia.

## Grafo y merge a dev

Ant-Man consulta archivos, símbolos, imports, dependencias y tests mediante el grafo
y OpenCode. El índice indica el SHA analizado y separa relaciones extraídas de las
inferidas. Para ramas activas se considera también su diff respecto del grafo base.

Cada merge a dev dispara una actualización incremental idempotente por repositorio
y SHA, delegada a Ant-Man o al adaptador configurado para refrescar el grafo. Debe
procesar cambios, eliminaciones y relaciones afectadas. Si falla, se marca obsoleto
y se reintenta; no se presenta como actualizado. La reconstrucción completa sirve
para reconciliar el índice.

La actualización del grafo y la verificación del deploy pueden correr en paralelo.
Jarvis registra las respuestas y sus SHA; merges posteriores generan actualizaciones
adicionales para identificar correctamente la revisión vigente.

## Entrega

Soldado del Invierno integra solo cuando los controles previos requeridos están aprobados y despliega el SHA integrado. Guardianes ejecutan los E2E contra ese SHA desplegado, con datos de prueba aislados. Un fallo de despliegue se informa según la política de recuperación del proyecto; un fallo E2E lo informa Guardianes y Jarvis lo enruta al responsable. Revertir código o datos exige considerar compatibilidad y migraciones.

El cierre requiere especificación cumplida, verificaciones del commit final, E2E
en dev ejecutados por Guardianes, artefactos registrados, actualización del grafo y evaluación final de memoria.
Pantera puede concluir que no hay reglas nuevas útiles: no se exige agregar memoria.



El cierre de tarea no detiene Jarvis: vuelve a atender pedidos en la misma sesión,
según el [contrato de supervisión](supervision.md).
