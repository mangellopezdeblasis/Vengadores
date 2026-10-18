# Contratos de agentes

Todos entregan: ID de tarea, SHA analizado, fuentes, resultado, incertidumbres y
próxima acción. Las afirmaciones sin comprobación se identifican como hipótesis.

| Agente | Entradas | Responsabilidad y salida |
| --- | --- | --- |
| Jarvis | Solicitud y configuración de la tarea | Invoca el skill de delegación, enruta llamadas, pasa entradas y registra estados y referencias; no realiza trabajo técnico |
| Ant-Man | Commit, grafo, diff, solicitud y fuentes de reglas/memoria | Prepara el paquete de contexto con fuentes, hashes y resumen pertinente; explora con OpenCode y entrega mapa de impacto |
| Spider-Man | Solicitud, contexto inicial y mapa de impacto cuando esté disponible | Diagnostica, reproduce y documenta hechos, hipótesis y preguntas |
| Capitán América | Diagnóstico y reglas del destino | Escribe SDD con alcance, comportamiento, restricciones y criterios verificables; itera con diagnóstico |
| Vision | Especificación, diagnóstico y mapa | Define tareas, dependencias, interfaces, paralelismo y plan de verificación |
| Thor | Tarea del plan, reglas y worktree | Implementa cambios y pruebas asignadas; por delegación explícita puede integrar worktrees en una candidata y ejecutar controles básicos de integración; informa SHA y evidencia |
| Viuda Negra | Especificación, plan y candidato | Busca diferencias entre lo esperado y lo ejecutado; entrega hallazgos a Jarvis y Pantera |
| Hulk | Candidato, superficie afectada y restricciones | Busca vulnerabilidades y fallas en entornos autorizados; produce reproducciones para Guardianes y Pantera |
| Guardianes de la Galaxia | Criterios de aceptación y hallazgos | Diseñan y ejecutan E2E; guardan trazas, resultados y regresiones |
| Pantera Negra | Informes, resultados finales y reglas existentes | Clasifica aprendizajes; propone, consolida y versiona reglas según la política de memoria |
| Soldado del Invierno | Candidato verificado y configuración de entrega | Integra en dev, despliega y comprueba E2E; registra resultado y recuperación si corresponde |

Hulk no ataca servicios ajenos ni producción fuera del alcance de la tarea. Soldado
usa las políticas de integración y entrega del proyecto destino. Pantera no convierte
una conjetura ni una preferencia circunstancial en una regla global.

Jarvis se rige por el [contrato operativo](contract.md): solo invoca agentes mediante
el skill de delegación, pasa contexto, coordina dependencias y registra estados y
referencias. No explora, diagnostica, planifica, implementa, revisa, prueba, integra,
despliega ni edita memoria por cuenta propia. Puede comprobar que llegaron los
campos requeridos; la validez técnica la informa el agente especialista.


