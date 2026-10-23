# Instalar y configurar Jarvis en un proyecto

Jarvis es una skill. El host la carga y ejecuta sus instrucciones con las herramientas
reales disponibles. Hay adaptadores para Codex con `collaboration` y para OpenCode
con `task`; si el host expone otro API, se bloquea sin inventar llamadas. El instalador copia Jarvis y Nick Fury, conserva separada la skill de
delegación y no levanta servicios ni cambia el código del destino.

## Instalación

1. Obtener una copia de la rama `docs/aprendizajes-orquestacion` de Vengadores y
   fijar la revisión que se usará. Requiere Python 3.9 o posterior.
2. Usar la skill `delegacion-vengadores` incluida o ubicar una skill externa compatible.
3. Agregar la carpeta de Vengadores al `PATH` de la terminal. Por ejemplo, guardar
   en `.bashrc` o `.zshrc` la línea `export PATH="/ruta/Vengadores:$PATH"`, usando
   la ruta real, y abrir una terminal nueva. Luego, desde el proyecto destino:

```bash
vengadores unidos --host codex --activate
```

`--activate` requiere `--host codex`; para OpenCode instalar con `vengadores unidos`
y seleccionar el agente primario Jarvis. El destino por defecto es el
directorio actual; puede elegirse otro con `--project /ruta/proyecto`. Se instala en `.opencode/skills/jarvis` o
`.agents/skills/jarvis`. La dependencia se instala al lado, en `delegacion-vengadores`,
y se vincula automáticamente. También instala `nick-fury` y guarda su referencia
en `author_skill`. Instala `escalacion-vengadores` y la vincula en
`escalation_skill`, con perfiles iniciales por rol y política de intervención.
Ver [escalada](escalada.md). OpenCode recibe `.opencode/agents/jarvis.md` y `nick-fury.md`,
que limita al coordinador a leer, cargar skills y delegar a `general` o `nick-fury`; no toca
`opencode.json`. Seleccionar el agente primario Jarvis en OpenCode.
Si ya existe una instalación, el programa la preserva;
`--replace` permite reemplazarla explícitamente. Un proyecto tiene un vínculo de
host activo en `.vengadores/jarvis.json`; cambiarlo requiere una reinstalación explícita.

4. Con `--activate`, si falta `.vengadores/config.yaml` se crea una configuración
   mínima (JSON válido como YAML 1.2), sin inventar dev, deploy ni presupuestos.
   Si existe, se conserva byte por byte, también con `--replace`. Adaptar después
   `templates/project/vengadores.yaml` sin sobrescribir esa configuración. Allí van reglas, memoria, comandos,
   permisos, presupuestos y validaciones reales. El vínculo de delegación vive
   únicamente en `.vengadores/jarvis.json`; no duplicar su ruta en YAML.
5. Ejecutar el chequeo y reabrir la sesión del host:

```bash
vengadores check --project /ruta/proyecto
```

`configurado` significa que los archivos y la dependencia tienen formato básico
válido. `host_execution: pendiente_de_invocacion_real` significa que todavía no se
comprobó ejecución. Si falta una dependencia, el chequeo termina con código 2 y
estado `bloqueado`. No ejecuta el contenido de la skill de delegación.

## Activación por worktree

Ejecutar instalación y activación en la raíz activa de cada worktree. La raíz del
checkout principal no activa sus worktrees automáticamente. `--activate` agrega un
bloque ROOT a `AGENTS.md` para Jarvis principal; no cambia el rol de los workers.
Si el instalador detecta `AGENTS.override.md`, atender el bloqueo antes de escribir.

En cada inicio o recuperación, ejecutar `vengadores check --project /ruta/worktree`
y comprobar instalación más activación efectiva de Codex, vínculo a la fuente canónica y
versión/hashes del contexto. La prueba estructural no demuestra recarga de una
sesión ya abierta: abrir una sesión nueva o cargar las fuentes explícitamente si
el host lo admite, conservando la advertencia de recarga pendiente.

En OpenCode, seleccionar el agente primario; `active: null` en el chequeo no
acredita esa selección.

Jarvis PRINCIPAL conserva la coordinación. No recuperarlo mediante un Jarvis hijo.
El [registro de workers](../skills/delegacion-vengadores/references/registry.md)
prepara el contrato antes de spawn, vincula el ID real después y comprueba identidad
antes de continuar el mismo encargo. El guard valida registro; no intercepta llamadas
directas fuera del adaptador ni acredita ejecución del host.

## Usar una skill externa

Por defecto se instala `delegacion-vengadores`. Para reemplazar su vínculo por otra
skill existente, agregar `--delegation-skill` a la instalación o ejecutar:

```bash
python3 scripts/configure_jarvis.py bind --project /ruta/proyecto --delegation-skill /ruta/real/delegacion/SKILL.md
```

El vínculo contiene rutas locales. Excluir `.vengadores/jarvis.json` del Git del
destino; no contiene credenciales y no debe agregársele ninguna. Una skill externa vinculada
sigue en su ubicación original. Para `--activate` debe distribuir
`scripts/worker_guard.py` junto a su `SKILL.md`; si falta, el instalador bloquea
antes de escribir. El adaptador debe usar la ruta real del helper de esa dependencia,
no asumir la ruta de la skill incluida. Ant-Man prepara el contexto de reglas y memorias,
sin sustituir los archivos originales del proyecto.

## Uso y comprobación real

Desde una sesión del host abierta en el destino: «Usá Jarvis para coordinar <tarea>».
Jarvis lee la skill de delegación y verifica que su interfaz exista. Una respuesta
real de un subagente debe incluir identificador, estado, revisión y evidencia.
El acceso a GitHub, la presencia de un archivo o aceptar una llamada no demuestran
que el agente haya terminado su trabajo.

Si la interfaz o los permisos no existen, Jarvis informa el bloqueo sin sustituir
al especialista ni simular delegaciones. El servicio de grafo, los sandboxes cloud
y las herramientas de tests/deploy se configuran por proyecto antes de sus etapas.
Los informes se guardan en `.vengadores/tasks/<id>/` o la ubicación del destino.
