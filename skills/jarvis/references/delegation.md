# Vinculación de la skill de delegación

El configurador del repositorio instala Jarvis y crea `.vengadores/jarvis.json`.
`delegation_skill` apunta por defecto a la skill incluida `delegacion-vengadores`,
instalada como hermana de Jarvis. Con `--delegation-skill` puede vincularse otra
skill externa. La interfaz se lee de la dependencia y se verifica frente al host.

Ejemplo de configuración creada por el instalador:

```json
{
  "schema_version": 1,
  "host": "opencode",
  "skill_directory": ".opencode/skills/jarvis",
  "delegation_skill": "/ruta/proyecto/.opencode/skills/delegacion-vengadores/SKILL.md"
}
```

Con la carpeta de Vengadores agregada al PATH de la terminal, instalar y vincular
desde el proyecto destino:

```bash
vengadores unidos
```

Para Codex, usar `vengadores unidos --host codex`; la ubicación es `.agents/skills/jarvis`.
Reabrir la sesión del host para que descubra la nueva skill. También puede abrirse
su `SKILL.md` explícitamente si el host permite cargar skills por ruta.

Si Jarvis ya está instalado, vincular la dependencia:

```bash
python3 scripts/configure_jarvis.py bind --project /ruta/proyecto --delegation-skill /ruta/real/delegacion/SKILL.md
python3 scripts/configure_jarvis.py check --project /ruta/proyecto
```

Si la dependencia se elimina o no existe, el estado es `bloqueado`. Vincular un archivo válido
comprueba su presencia y formato; la compatibilidad de sus herramientas se comprueba
en el host al activar Jarvis. No se ejecutan scripts arbitrarios de la dependencia.

La configuración de vínculo es local y no debe llevar rutas privadas al repositorio.
Los comandos, permisos, presupuestos y datos del proyecto pertenecen a su configuración
general. El vínculo no amplía permisos ni instala herramientas de ejecución.

## Activación en la raíz activa

Instalación y activación se verifican en la raíz del worktree donde se ejecuta
Jarvis, a cada inicio o recuperación. La instalación del checkout principal no
cubre automáticamente otros worktrees. Usar la revisión canónica elegida y
conservar su vínculo, versión y hashes de contexto; Ant-Man prepara las fuentes
aplicables del destino sin copiar datos privados a Vengadores.

Desde un ejecutor autorizado, instalar/actualizar y activar explícitamente:

```bash
vengadores unidos --project /ruta/worktree --host codex --activate
vengadores check --project /ruta/worktree
```

Para reemplazar una instalación existente, agregar `--replace` tras conservar
personalizaciones. `--activate` instala un bloque ROOT en `AGENTS.md` de esa raíz
para el agente principal; no asigna Jarvis a workers. Una instrucción conflictiva
como `AGENTS.override.md` debe resolverse según el error del instalador antes de
considerar activación válida; no omitirla ni sobrescribirla silenciosamente.

En Codex, `check` distingue instalación y activación efectiva de la raíz. En
OpenCode la activación requiere seleccionar el agente primario en la interfaz;
`active: null` no acredita esa selección ni es una prueba de activación. No acredita que
una sesión abierta haya recargado instrucciones: abrir una sesión nueva o cargar
explícitamente las fuentes si el host lo admite y volver a comprobar. Conservar
la advertencia sobre sesiones existentes. La prueba real inocua del protocolo
sigue siendo necesaria para afirmar delegación funcional.

La activación requiere configuración local, helper de registro y bloque ROOT sin
`AGENTS.override.md`. `--activate` crea configuración mínima solo si falta y
preserva íntegramente la existente. Una delegación externa debe incluir su propio
`scripts/worker_guard.py`; de lo contrario se bloquea antes de escribir. Usar su
ruta real, no la ubicación supuesta de la dependencia distribuida.
