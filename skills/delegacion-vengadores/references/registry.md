# Registro de identidad de workers

El helper distribuido `scripts/worker_guard.py` pertenece a esta skill. Ejecutarlo
con Python desde la raíz activa del worktree, usando el directorio instalado de
la skill (`.agents/skills/delegacion-vengadores` en Codex,
`.opencode/skills/delegacion-vengadores` en OpenCode). No usar la instalación
de otro checkout como evidencia de activación local.

## Despacho

Antes de una llamada real del host:

```bash
python3 .agents/skills/delegacion-vengadores/scripts/worker_guard.py prepare --project /ruta/worktree --role thor --task T1 --version REV --context-ref /ruta/artefacto --fork-turns none
```

`--context-ref` se repite para cada fuente pertinente. La salida contiene un ticket
UUID, rol, tarea, workspace, versión, referencias, `fork_turns`, `worker_id: null`,
estado `planificado` y `host_execution: no_verificado`; en un repositorio registra
también `git_commit` real. Los roles usan identificador ASCII en minúscula y
`jarvis` se rechaza como worker. Conservar el ticket.
El prompt de spawn contiene el contrato autosuficiente del protocolo y su rol/tarea.

Después de `collaboration.spawn_agent`, vincular el ID real devuelto:

```bash
python3 .agents/skills/delegacion-vengadores/scripts/worker_guard.py bind --project /ruta/worktree --ticket UUID --worker-id /root/ID_REAL
```

No inventar IDs ni registrar ejecución porque `prepare` o `bind` terminan bien.
Los estados y resultados del host son la evidencia de ejecución.

## Continuación y fallos

Antes de `followup_task`, comprobar las mismas invariantes:

```bash
python3 .agents/skills/delegacion-vengadores/scripts/worker_guard.py resume --project /ruta/worktree --ticket UUID --role thor --task T1 --version REV
```

Usar el mismo ID devuelto solo para continuar/corregir el encargo. Si cambió la
versión o HEAD del repositorio, reconciliar el contrato y preparar una sesión nueva cuando el registro
rechace esa continuación; no alterar campos para eludirlo. Para otro rol/tarea,
crear otro ticket y worker con traspaso mínimo.

Errores terminan con código 2 y estado `bloqueado`: conservar el error y no hacer
la llamada prevista. Si spawn falla, conservar la preparación como no verificada;
si bind falla después de un spawn real, informar el ID real y reconciliar el
registro antes de nuevas acciones. No repetir spawn para ocultar ese fallo.

El helper registra y valida identidad; no inicia agentes, cambia permisos/modelos
ni comprueba resultados técnicos. No puede impedir una llamada directa a las
herramientas del host fuera de este adaptador. En OpenCode los permisos instalados deniegan shell al coordinador: no asumir
que puede ejecutar el helper. Requiere un ejecutor real autorizado
para estos comandos de coordinación; si el host lo deniega, informar bloqueo sin
simular el registro ni dar al coordinador permisos generales de ingeniería.

El registro usa lock exclusivo y reemplazo atómico del archivo. Un crash puede
dejar `workers.lock`: limpiar ese lock solo después de comprobar que no hay una
mutación del registro en curso. No quitarlo para forzar una llamada concurrente.
