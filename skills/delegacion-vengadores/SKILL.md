---
name: delegacion-vengadores
description: Inicia y reanuda subagentes reales para Jarvis. Usar al delegar tareas mediante Codex collaboration u OpenCode task.
---

# Delegación

Usá únicamente herramientas presentes y autorizadas. No simules agentes, ejecutes
su trabajo ni amplíes permisos. Leé el host en `.vengadores/jarvis.json` y solo su
adaptador: [Codex](references/codex.md) u [OpenCode](references/opencode.md).

1. Recibí ID, rol, objetivo, revisión, alcance, entradas, aceptación y límites.
   La preparación de contexto se delega a Ant-Man; no inventes fuentes o SHA.
2. Pasá contexto pertinente y pedí estado, revisión, resultado, evidencia,
   incertidumbres y próxima acción. Los workers no redelegan sin autorización.
3. Aplicá el perfil solicitado solo con controles reales del host; registrá lo
   solicitado, aplicado y desconocido según `escalation_skill`.
   Iniciá la llamada real y guardá su ID. Esperá su respuesta con el host;
   aceptación no es finalización. Paralelizá solo unidades independientes autorizadas.
4. Reanudá la misma sesión para correcciones. Respetá límites de concurrencia,
   costo, tiempo y reintentos. Ante una dependencia ausente o denegación, bloqueá.
5. Para editar, exigí un worktree propio y propiedad de recursos. Si falta,
   delegá su preparación antes de lanzar workers. Worktree no equivale a sandbox.
6. Confirmá el resultado recibido; falta de evidencia, timeout o cancelación no
   equivalen a aprobación. El cierre de un worker no detiene al supervisor.

Para preparar worktrees, contratos de respuesta o interrupciones: [protocolo](references/protocol.md).
Antes de afirmar ejecución funcional, delegá una lectura inocua y registrá ID y
respuesta reales. Esa prueba no acredita otros hosts, paralelismo, grafo ni deploy.
