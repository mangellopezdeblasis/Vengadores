# Validación de Jarvis y delegación

Fecha: 18 de octubre de 2026. Rama: `docs/aprendizajes-orquestacion`.

## Instalador

Se ejecutó `python3 -m unittest discover -s tests -v`: doce pruebas aprobadas.
Cubren instalación en Codex/OpenCode, dependencia separada por defecto, vínculo
externo, dependencia ausente, preservación de instalaciones y agentes existentes,
fallos previos a escribir, rechazo de auto-delegación y detección de instalación
incompleta si falta el contrato de supervisión. Las tres pruebas del comando
`vengadores unidos` comprueban el destino actual con espacios, la selección de Codex
y la preservación de trabajo existente, ejecutando el comando real como subproceso.

La instalación real se comprobó en el workspace para ambos hosts con `check`.
Este comando solo evalúa estructura y dependencias en disco. No recibe ni concede
permisos de herramientas ni reemplaza una delegación real.

## Delegación real en Codex

- ID lógico: `JARVIS-SMOKE-001`.
- ID de agente devuelto por el host: `/root/jarvis_smoke`.
- Adaptador: `collaboration.spawn_agent`, sin heredar el historial completo.
- Rol: Ant-Man, tarea de lectura de las skills y su vínculo de configuración.
- Resultado del worker: `completado`; confirmó que `jarvis.json` vincula la skill
  Jarvis con la skill separada `delegacion-vengadores` para el host Codex.
- El worker informó `writes_performed: false`, evidencia de los archivos leídos
  y sus límites. La revisión Git del staging no se afirmó como verificada.

Se reanudó la misma sesión con `collaboration.followup_task` para
`JARVIS-SMOKE-002`. El worker volvió a informar `completado` sin escrituras y confirmó
el modo de comprobación de instalación de la versión final. SHA256 de Jarvis
instalado: `06bc0fa5f429a2e0cad3312f7e815f9f23f3ef7c490c513ebcb4986d15c2d534`.

El recibo real fue recibido en la conversación del coordinador. No es una respuesta
simulada ni un test con una herramienta de delegación falsa.

## Supervisor que conserva la sesión

Se inició `/root/jarvis_supervisor` como Jarvis con autorización explícita de
profundidad dos y un worker concurrente. Se le dieron dos pedidos consecutivos:

| Pedido | Especialista real | Resultado informado |
| --- | --- | --- |
| SUP-001 | `/root/jarvis_supervisor/ant_man_sup_001` | Leyó el encabezado de README.md; completado. |
| SUP-002 | `/root/jarvis_supervisor/spider_man_sup_002` | Leyó una regla de AGENTS.md; completado. |

El segundo pedido se envió mediante `followup_task` al mismo supervisor, que
conservó SUP-001 y no la repitió. Ambos recibos informaron el mismo supervisor_id
y terminaron en `supervisor_state: esperando_usuario`. Las tareas fueron de
lectura, con revisión null por staging local, sin ejecución del flujo técnico.

Esto valida dos delegaciones sucesivas desde una sesión de supervisor conservada
en Codex. La sesión queda disponible para más pedidos del host; no acredita un
proceso escuchando fuera de ella ni permanencia después de cerrar la aplicación.
Las reglas de pausa/detención están configuradas; no se simuló una cancelación
real de procesos o de infraestructura.

## Límites

OpenCode no estaba instalado en este entorno. Su adaptador y agente primario se
prepararon con referencia a [documentación oficial](https://opencode.ai/docs/agents/)
y al esquema básico de Task, pero su ejecución debe validarse en el host destino.
Esta prueba no acredita worktrees concurrentes, sandboxes, grafo, E2E, despliegues
ni la ejecución completa de todos los roles. Esas capacidades dependen del proyecto.
