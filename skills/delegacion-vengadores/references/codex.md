# Adaptador Codex con herramientas collaboration

Usar solo si estas herramientas están realmente disponibles. No toda sesión de
Codex tiene el mismo API; otro API requiere un adaptador explícito y comprobado.

1. Aplicar `prepare` del [registro](registry.md) antes de iniciar con `collaboration.spawn_agent`: `task_name` estable (minúsculas, números
   y guion bajo), `message` con el contrato y `fork_turns: "none"` para enviar solo
   las entradas necesarias. Incluir en el mensaje todo lo que el worker necesita.
   No sobrescribir modelo o esfuerzo sin instrucción del usuario o proyecto.
2. Aplicar `bind` con el ticket y el identificador real devuelto. Para concurrencia independiente, iniciar
   varias llamadas antes de esperar, dentro del límite autorizado.
3. Los mensajes y la respuesta final llegan al coordinador. `collaboration.wait_agent`
   espera notificaciones, pero no convierte la notificación en un informe completo.
   Usar esperas acotadas y comunicar progreso al usuario durante trabajos largos.
4. Para continuar o corregir el mismo rol y tarea de un agente inactivo, validar
   primero `resume` del registro y usar `collaboration.followup_task` con el ID real
   devuelto y un delta con referencias. Para otro rol/tarea, preparar y lanzar un
   worker nuevo con traspaso mínimo. Para enviar contexto del mismo encargo a uno
   activo, usar `collaboration.send_message`; no inicia a uno inactivo.
5. Consultar `collaboration.list_agents` cuando sea necesario para resolver el
   estado; no hacer bucles de polling. `collaboration.interrupt_agent` detiene su
   turno actual si hace falta, pero no acredita limpieza de procesos o recursos.

Estas herramientas se llaman directamente en el host; no están dentro de
`functions.exec`. Los subagentes comparten el filesystem de esta familia de hosts.
La propiedad de archivos y los worktrees deben prepararse por delegación antes
de lanzar tareas que escriban en paralelo. No inferir límites de sandbox distintos.

## Supervisor conservado

Jarvis es el agente PRINCIPAL y único decisor de coordinación. Recupera el registro
y los IDs en esa sesión; no lanzar un worker Jarvis para recuperar al supervisor.
Los especialistas conservan un rol y tarea fijos según el protocolo. Cuando no hay
llamadas pendientes, Jarvis devuelve `esperando_usuario` y el host conserva su
sesión. No mantener una espera infinita ni afirmar ejecución fuera del host.

## Perfiles portables

La política de `escalation_skill` es instrucción del proyecto para solicitar perfiles.
`basico/estandar/avanzado` y `bajo/medio/alto` no son identificadores nativos.
Heredá el modelo al no disponer de una resolución autorizada del host. Inspeccioná
el esquema disponible: usá `model`/`reasoning_effort` solo si existen, con valores
admitidos y resolución documentada por el entorno; no inferir capacidad por nombre.
No crear una matriz de modelos en esta skill ni inventar un servicio de selección.
Si la interfaz no permite overrides al continuar, una escalada efectiva necesita
una nueva sesión con contexto mínimo y entrega controlada de recursos.
Guardá IDs anterior/nuevo. Un parámetro solicitado es evidencia de solicitud, no de
que el proveedor lo aplicó; si el host no lo confirma, registrá aplicado null.
Sin selección/resolución disponible, notificá perfil no garantizado. Si es obligatorio,
bloqueá antes de ejecutar; si es preferencia inicial, se permite heredar con aviso.
