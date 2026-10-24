---
name: delegacion-vengadores
description: Inicia y reanuda subagentes reales para Jarvis. Usar al delegar tareas mediante Codex collaboration u OpenCode task.
---

# Delegación

Usá únicamente herramientas presentes y autorizadas. No simules agentes, ejecutes
su trabajo ni amplíes permisos. Jarvis PRINCIPAL coordina; cada worker conserva
un rol/tarea, sin asumir Jarvis ni redelegar. Leé `.vengadores/jarvis.json` y su
adaptador: [Codex](references/codex.md) u [OpenCode](references/opencode.md).

1. Recibí ID, rol, objetivo, revisión, alcance, entradas, aceptación y límites.
   La preparación de contexto se delega a Ant-Man; no inventes fuentes o SHA.
2. Prepará un prompt autosuficiente con reglas esenciales, referencias y versiones;
   Codex siempre usa `fork_turns: "none"`. Pedí el recibo mínimo del protocolo.
3. Aplicá el perfil solicitado solo con controles reales del host; registrá lo
   solicitado, aplicado y desconocido según `escalation_skill`.
   Validá el registro antes de spawn y vinculá después el ID real, según adaptador.
   Esperá con el host; aceptación no es finalización. Solo paralelizá lo autorizado.
4. Antes de reanudar validá rol/tarea/versiones en el registro. Solo continuá o
   corregí el mismo encargo con deltas y referencias; otro rol exige worker nuevo
   y traspaso mínimo. Respetá límites; ante dependencia ausente o denegación, bloqueá.
5. Para editar, exigí un worktree propio y propiedad de recursos. Si falta,
   delegá su preparación antes de lanzar workers. Worktree no equivale a sandbox.
6. Confirmá el resultado recibido; falta de evidencia, timeout o cancelación no
   equivalen a aprobación. El cierre de un worker no detiene al supervisor.

Para preparar worktrees, contratos de respuesta o interrupciones: [protocolo](references/protocol.md).
Antes de afirmar ejecución funcional, delegá una lectura inocua y registrá ID y
respuesta reales. Esa prueba no acredita otros hosts, paralelismo, grafo ni deploy.
