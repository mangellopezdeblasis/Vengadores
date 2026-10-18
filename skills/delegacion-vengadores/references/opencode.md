# Adaptador OpenCode

Usar la herramienta nativa `task` cuando el host la exponga y permita invocar un
subagente. El rol Vengadores se pasa en el prompt; no es automáticamente el nombre
de un agente instalado.

La interfaz básica documentada tiene `description`, `prompt` y `subagent_type`.
Usar `subagent_type: "general"` si ese agente existe y sus permisos sirven para
la tarea. Para continuar una sesión, pasar el `task_id` real devuelto previamente.
Verificar el esquema que expone el host antes de llamar; si difiere, informar el
bloqueo en vez de inventar parámetros.

La llamada normal espera el resultado. Solicitudes independientes pueden ir en
un mismo lote si el host admite ejecución paralela; si no, se ejecutan en serie
y se declara esa limitación. No exigir ni activar modos background experimentales.
No hay una API portable de cancelación asumida por esta skill: usar solo la que
exponga el host, o informar al usuario cómo interrumpir en su interfaz.

El worker debe recibir la ruta de su worktree y usarla para comandos y ediciones.
La herramienta Task no garantiza por sí sola sandboxes ni worktrees diferentes.

El instalador agrega un agente primario `.opencode/agents/jarvis.md`. Sus permisos
impiden al coordinador ejecutar shell o editar archivos; permite cargar skills,
leer configuración y llamar a `general` o al autor `nick-fury`. Los permisos del proyecto y
del proveedor siguen aplicando a los workers. No se modifica `opencode.json`.

Fuentes primarias consultadas para esta interfaz (18 de octubre de 2026):

- [Agentes y permisos de OpenCode](https://opencode.ai/docs/agents/)
- [Skills de OpenCode](https://opencode.ai/docs/skills/)
- [Implementación de Task](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/tool/task.ts)

No se probó OpenCode en el entorno de creación porque su CLI no estaba instalado.
La validación real debe ejecutarse al abrir una sesión OpenCode en el destino.

El agente primario Jarvis conserva el rol al finalizar cada tarea. Los resultados
y nuevos mensajes se atienden dentro de la misma conversación. No crear un nuevo
Jarvis para cada pedido ni confundir la respuesta final de un worker con el cierre
del supervisor. La aplicación controla la disponibilidad y conservación de sesión.
