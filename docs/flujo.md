# Flujo de Jarvis

## Estados y avance

| Estado | Responsable | Entregable / condición para avanzar |
| --- | --- | --- |
| Preparación | Jarvis | ID de tarea, commit base, configuración, reglas, memoria resumida y versión del grafo |
| Investigación | Ant-Man y Spider-Man en paralelo | Mapa de impacto y diagnóstico con evidencia |
| Especificación | Capitán América ↔ Spider-Man | Criterios verificables y decisiones resueltas; Ant-Man aporta contexto |
| Planificación | Vision | Tareas, dependencias, contratos compartidos y verificaciones |
| Implementación | Uno o varios Thor | Cambios por tarea en ramas y worktrees propios |
| Integración candidata | Jarvis | Cambios reunidos, conflictos resueltos y verificaciones básicas aprobadas |
| Revisión | Viuda Negra y Hulk en paralelo | Conformidad con especificación/plan y hallazgos adversariales |
| E2E candidata | Guardianes de la Galaxia | Recorridos de aceptación y regresiones de Hulk ejecutados |
| Aprendizaje propuesto | Pantera Negra | Ajustes de reglas clasificados por destino, con evidencia |
| Integración y deploy | Soldado del Invierno | Merge a dev, despliegue del commit integrado y E2E del despliegue |
| Cierre | Jarvis y Pantera Negra | Resultado final, grafo actualizado y aprendizajes validados/versionados |

Jarvis usa el skill de delegación existente para iniciar y coordinar agentes. Los
agentes no necesitan compartir el historial completo: reciben reglas pertinentes,
entradas de su etapa y referencias a los artefactos.

## Paralelismo y worktrees

- Vision define unidades independientes y acuerda primero los contratos compartidos.
- Cada Thor tiene rama y worktree propios, derivados de un commit base identificado.
- Cada sandbox cloud puede tener su propio clon y crear allí su worktree.
- Un worktree no aísla procesos, red ni credenciales: la ejecución requiere sandboxes.
- Jarvis coordina archivos compartidos y evita escrituras concurrentes sobre el mismo worktree.
- La revisión conjunta ocurre sobre la rama candidata, no solo sobre cambios individuales.
- Al cambiar el commit revisado se invalidan los controles afectados. Antes del merge,
  comprobar que los resultados corresponden al candidato final y a la base dev actual.

## Correcciones y bloqueos

Jarvis envía cada hallazgo al responsable de su causa:

| Causa | Retorno |
| --- | --- |
| Contexto o impacto incorrectos | Ant-Man |
| Diagnóstico sin evidencia suficiente | Spider-Man |
| Ambigüedad de comportamiento | Capitán América ↔ Spider-Man |
| Plan incompleto o dependencia omitida | Vision |
| Implementación defectuosa | Thor |
| Decisión de producto ausente | Responsable humano de la tarea |

Después de una corrección se repiten las verificaciones afectadas. Jarvis limita
iteraciones, tiempo y presupuesto según configuración. Alcanzar el límite produce
un bloqueo con evidencia; no equivale a éxito. Los controles son estados verificados,
no una conclusión libre del modelo.

## Grafo y merge a dev

Ant-Man consulta archivos, símbolos, imports, dependencias y tests mediante el grafo
y OpenCode. El índice indica el SHA analizado y separa relaciones extraídas de las
inferidas. Para ramas activas se considera también su diff respecto del grafo base.

Cada merge a dev dispara una actualización incremental idempotente identificada por
repositorio y SHA. Debe procesar cambios, eliminaciones y relaciones afectadas. Si
el índice falla, se marca desactualizado y se reintenta; no se presenta como actual.
La reconstrucción completa queda disponible para reconciliar el índice.

La actualización del grafo y la verificación del deploy pueden correr en paralelo.
Jarvis registra ambos resultados por separado y contempla merges posteriores para
no confundir el SHA de la tarea con el estado más reciente de dev.

## Entrega

Soldado del Invierno integra solo cuando los controles requeridos están aprobados.
Ejecuta E2E contra el despliegue del SHA integrado, con datos de prueba aislados.
Un fallo del deploy o de E2E deja la tarea fallida y activa la política de recuperación
del proyecto. Revertir código o datos exige considerar compatibilidad y migraciones.

El cierre requiere especificación cumplida, verificaciones del commit final, E2E
en dev, artefactos registrados, actualización del grafo y evaluación final de memoria.
Pantera puede concluir que no hay reglas nuevas útiles: no se exige agregar memoria.

