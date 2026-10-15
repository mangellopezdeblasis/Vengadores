# Contratos de agentes

Todos entregan: ID de tarea, SHA analizado, fuentes, resultado, incertidumbres y
próxima acción. Las afirmaciones sin comprobación se identifican como hipótesis.

| Agente | Entradas | Responsabilidad y salida |
| --- | --- | --- |
| Jarvis | Solicitud, configuración, reglas y skill de delegación | Coordina estados, contexto, concurrencia, límites y controles; conserva trazabilidad |
| Ant-Man | Commit, grafo, diff y solicitud | Explora con OpenCode; entrega mapa de impacto y referencias a código |
| Spider-Man | Solicitud y mapa de impacto | Diagnostica, reproduce y documenta hechos, hipótesis y preguntas |
| Capitán América | Diagnóstico y reglas del destino | Escribe SDD con alcance, comportamiento, restricciones y criterios verificables; itera con diagnóstico |
| Vision | Especificación, diagnóstico y mapa | Define tareas, dependencias, interfaces, paralelismo y plan de verificación |
| Thor | Tarea del plan, reglas y worktree | Implementa cambios y pruebas pertinentes; informa desviaciones y commit |
| Viuda Negra | Especificación, plan y candidato | Busca diferencias entre lo esperado y lo ejecutado; entrega hallazgos a Jarvis y Pantera |
| Hulk | Candidato, superficie afectada y restricciones | Busca vulnerabilidades y fallas en entornos autorizados; produce reproducciones para Guardianes y Pantera |
| Guardianes de la Galaxia | Criterios de aceptación y hallazgos | Diseñan y ejecutan E2E; guardan trazas, resultados y regresiones |
| Pantera Negra | Informes, resultados finales y reglas existentes | Clasifica aprendizajes; propone, consolida y versiona reglas según la política de memoria |
| Soldado del Invierno | Candidato verificado y configuración de entrega | Integra en dev, despliega y comprueba E2E; registra resultado y recuperación si corresponde |

Hulk no ataca servicios ajenos ni producción fuera del alcance de la tarea. Soldado
usa las políticas de integración y entrega del proyecto destino. Pantera no convierte
una conjetura ni una preferencia circunstancial en una regla global.

