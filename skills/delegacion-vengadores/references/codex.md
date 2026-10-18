# Adaptador Codex con herramientas collaboration

Usar solo si estas herramientas están realmente disponibles. No toda sesión de
Codex tiene el mismo API; otro API requiere un adaptador explícito y comprobado.

1. Iniciar con `collaboration.spawn_agent`: `task_name` estable (minúsculas, números
   y guion bajo), `message` con el contrato y `fork_turns: "none"` para enviar solo
   las entradas necesarias. Incluir en el mensaje todo lo que el worker necesita.
   No sobrescribir modelo o esfuerzo sin instrucción del usuario o proyecto.
2. Guardar el identificador devuelto. Para concurrencia independiente, iniciar
   varias llamadas antes de esperar, dentro del límite autorizado.
3. Los mensajes y la respuesta final llegan al coordinador. `collaboration.wait_agent`
   espera notificaciones, pero no convierte la notificación en un informe completo.
   Usar esperas acotadas y comunicar progreso al usuario durante trabajos largos.
4. Para trabajo nuevo o correcciones de un agente inactivo, usar
   `collaboration.followup_task` con `target` y `message`. Para enviar contexto a uno
   que ya trabaja, usar `collaboration.send_message`; no inicia a uno inactivo.
5. Consultar `collaboration.list_agents` cuando sea necesario para resolver el
   estado; no hacer bucles de polling. `collaboration.interrupt_agent` detiene su
   turno actual si hace falta, pero no acredita limpieza de procesos o recursos.

Estas herramientas se llaman directamente en el host; no están dentro de
`functions.exec`. Los subagentes comparten el filesystem de esta familia de hosts.
La propiedad de archivos y los worktrees deben prepararse por delegación antes
de lanzar tareas que escriban en paralelo. No inferir límites de sandbox distintos.
