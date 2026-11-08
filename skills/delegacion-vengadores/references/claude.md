# Adaptador Claude Code

Usar la herramienta nativa `Agent` cuando el host la exponga. El instalador
(`vengadores unidos --host claude`) genera un subagente por rol en
`.claude/agents/<rol>.md`; cada uno remite a su identidad del catálogo.

1. Aplicar `prepare` del [registro](registry.md) antes de llamar a `Agent` con
   `subagent_type` igual al rol (por ejemplo `thor`), `description` breve y
   `prompt` autosuficiente: tarea, revisión, habilidad, reglas esenciales,
   referencias y recibo esperado. El subagente no recibe el historial de Jarvis.
2. Aplicar `bind` con el identificador real que devuelva el host. Sin ID real,
   registrar el bloqueo; no inventarlo.
3. Para tareas que editan en Ultron/Thanos, usar el worktree preparado por
   delegación o, si el host lo ofrece, `isolation: "worktree"`. Registrar la ruta
   y rama resultantes. Un worktree no aísla red, procesos ni credenciales.
4. Para continuar el mismo rol y tarea, validar `resume` y enviar el delta al ID
   real con el mecanismo de continuación que exponga el host (por ejemplo
   `SendMessage`). Otro rol o tarea exige un `Agent` nuevo con traspaso mínimo.
5. Llamadas independientes pueden ir en un mismo turno si están autorizadas. Las
   que corren en segundo plano notifican al terminar: no hacer polling.

Verificar el esquema que expone el host antes de llamar. Si los parámetros
difieren o la herramienta no existe, informar el bloqueo en vez de inventarlos.
Los subagentes de Claude Code no pueden lanzar otros subagentes; Jarvis sigue
siendo el único coordinador en la sesión principal.

## Activación y supervisor

`--activate` agrega un bloque administrado a `CLAUDE.md` para que la sesión
principal aplique `.claude/skills/jarvis/SKILL.md`. No modifica
`.claude/settings.json` ni permisos: restringir escritura o shell del coordinador
queda a cargo del proyecto. Abrir una sesión nueva para que se cargue el bloque.

## Perfiles portables

Aplicá `escalation_skill`. Un `model` por llamada o en el subagente solo se usa
si el host lo admite y la selección está permitida; el instalador no fija
modelos. Registrar solicitado y aplicado por separado, aplicado null sin
confirmación del host. Para el perfil económico obligatorio de Thor en Loki, si
no puede seleccionarse y confirmarse un modelo de menor coste, bloquear Thor.

## Estado de validación

Esta interfaz se basa en las herramientas `Agent` y `SendMessage` de Claude Code.
No se ejecutó una delegación real con este adaptador: la primera tarea debe
delegar una lectura inocua y registrar ID y respuesta reales.
