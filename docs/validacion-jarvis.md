# Validación de Jarvis y delegación

Fecha: 18 de octubre de 2026. Rama: `docs/aprendizajes-orquestacion`.

## Instalador

Se ejecutó `python3 -m unittest discover -s tests -v`: veinte pruebas aprobadas.
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
instalado en esa prueba inicial: `06bc0fa5f429a2e0cad3312f7e815f9f23f3ef7c490c513ebcb4986d15c2d534`.

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

## Nick Fury y núcleos mínimos

Se incorporaron pruebas del auditor y de instalación de Nick Fury. La suite completa
alcanzó veinte pruebas aprobadas. Cada instalación incluye la skill de autor y, en
OpenCode, su perfil de subagente, preservando los agentes existentes salvo reemplazo
explícito. El auditor no convierte tamaño a tokens y sus presupuestos son avisos.

Jarvis conservó el supervisor `/root/jarvis_supervisor` y delegó `NF-AUDIT-001` a
`/root/jarvis_supervisor/nick_fury_nf_audit_001`. Nick Fury cargó su skill instalada
y ejecutó el auditor real sobre las tres skills: código 0, sin errores ni avisos.
Informó cuerpo de 212 palabras para Jarvis, 202 para delegación y 184 para Nick Fury;
los tokens quedaron null. La tarea fue de lectura; no acredita calidad de nuevas
skills generadas, ejecución OpenCode ni ahorro de tokens. Se conserva la investigación
y sus fuentes en [diseño de skills](investigacion-skills.md).

## Perfiles y escalada — 19 de octubre de 2026

ESC-001: Jarvis delegó autoría a Nick Fury en la sesión real
`/root/jarvis_supervisor/nick_fury_token_setup_001`. Se integraron su skill, política,
perfiles de doce roles y guía. El staging no tenía Git: se autorizó copia aislada
en /tmp y entrega revisable, sin afirmar que fuera un worktree. Revisión local null.

La suite `python3 -m unittest discover -s tests -v` pasó 23 pruebas. Los nuevos
controles cubren distribución de escalada en ambos hosts, ausencia de política,
rechazo de perfiles inválidos y preservación de una skill de escalada existente
antes de escribir el resto de la instalación. Se reinstaló realmente en los
destinos locales Codex y OpenCode; el chequeo devolvió configurado con
`escalation_skill` separado. No se ejecutó la CLI de OpenCode.

Auditor estructural: Jarvis 249 palabras de cuerpo, delegación 220 y escalada 200;
las tres skills sin errores ni avisos. Tokens no medidos. La política se ejecuta
como instrucciones del host y sus adaptadores; no se agregó un router autónomo.
No se verificó un cambio efectivo de modelo/esfuerzo, consumo, ahorro ni reservas
concurrentes en un backend persistente. El registro de sesión pertenece a Jarvis,
que serializa reservas y bloquea si pierde su evidencia.

El supervisor real `/root/jarvis_supervisor` recargó la instalación Codex y devolvió
`estado: configuracion_cargada`: encontró `escalation_skill` y los perfiles, con
Jarvis declarado basico/bajo. Confirmación del host, modelo, esfuerzo efectivo y
costo quedaron null. No creó workers ni pidió upgrades; regresó a esperando_usuario.
Este recibo acredita lectura de la configuración vinculada, no selección de modelo.

## Auditoría de seguridad de Hulk y recuperación de catálogo

Se adaptó Cloudflare security-audit-skill (MIT), commit
`c1c8a8c1471069fb0e188eeaff69b8e8db6564a8`, a
`subagentes/hulk/habilidades/auditoria-seguridad`. Se conservaron sus 22 archivos
originales con licencia y hashes de blobs en SOURCE.json. La adaptación distribuye
la coordinación exclusivamente a Jarvis y el trabajo técnico a workers separados.

La publicación previa de E2E utilizó una base antigua y reemplazó accidentalmente
archivos ajenos al cambio. Esta actualización recupera los archivos de la revisión
`d6cda509bd03ae893ececc35cc1b2bb7e25bac25` salvo los nueve documentos modificados
para asignar a Guardianes los E2E del despliegue, que se conservan desde
`5f134da25a673662fa7e6f26b3d8d067c892a060`. Se restablecen catálogo, activación ROOT,
registro de workers y sus controles; las modificaciones de esta habilidad se aplican
sobre esa recuperación, sin revertir el cambio de responsabilidades de E2E.

Validación: 36 tests Python aprobados, incluida copia de skill/licencia/validadores
en Codex y OpenCode y detección de recursos faltantes. El núcleo tiene 217 palabras;
auditor estructural sin errores ni avisos. Tokens no medidos.

Tests originales Node ejecutados directamente: findings 20/34 aprobados y ledger
21/31 aprobados; 24 casos fallaron en este entorno. Las invocaciones de procesos
Node hijos están bloqueadas con EPERM, confirmado con una llamada mínima a spawnSync.
La suite completa upstream NO se declara aprobada. Ambos validadores ejecutados
directamente aceptaron documentos vacíos de formato correcto (0 findings y 0 unidades);
esto no acredita una auditoría real ni cobertura. No se modificó el código upstream.

Nick Fury redactó la adaptación mediante delegación real HULK-AUDIT-001 en
`/root/jarvis_supervisor/nick_fury_token_setup_001`, con copia aislada autorizada
y revisión local null. No se auditó un target ni se ejecutó código de un target,
no se comprobó el sandbox requerido ni se midieron costos o ahorros.
