# Vengadores

Software Factory Agentic. Flujo reutilizable coordinado por **Jarvis**.
Los agentes usan OpenCode y el skill de delegación existente. La ejecución prevista es en cloud, con ramas y worktrees aislados para tareas concurrentes.

## Estado

Versión inicial: diseño del flujo, contratos y plantillas. Este repositorio no implementa un runtime, un servicio de grafo, automatización de GitHub ni deploys. Jarvis es el nombre del orquestador; su tecnología queda pendiente. No requiere eve.

## Documentación

- [Flujo y controles](docs/flujo.md)
- [Roles de los agentes](agents/roles.md)
- [Contrato operativo de Jarvis](agents/jarvis.md)
- [Reglas y memoria](docs/memoria.md)
- [Adopción en proyectos](docs/adopcion.md)
- [Plantilla de configuración](templates/project/vengadores.yaml)
- [Plantilla de memoria local](templates/project/memory.md)
- [Contrato de una tarea](templates/task/tarea.md)

## Uso en cualquier proyecto

1. Elegir un commit o tag de Vengadores y registrar esa versión en el proyecto destino.
2. Adaptar `templates/project/vengadores.yaml` a su stack y comandos reales.
3. Referenciar el skill de delegación existente. No se suministra un reemplazo.
4. Conservar `AGENTS.md`, la memoria y las reglas propias del destino; no sobrescribirlas.
5. Crear una tarea con `templates/task/tarea.md` y seguir el flujo de Jarvis.

Cada proyecto conserva su código, especificaciones, informes y memoria. Vengadores conserva reglas reutilizables de coordinación y aprendizaje. Las reglas se cargan por relevancia, sin enviar toda la documentación a cada agente.

Repositorio central: [mangellopezdeblasis/Vengadores](https://github.com/mangellopezdeblasis/Vengadores).
No se eligió una licencia de distribución ni una plataforma cloud todavía.
