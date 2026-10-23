# Vengadores

Software Factory Agentic coordinada por **Jarvis**, distribuido como una skill
instalable para OpenCode o Codex. Jarvis solo delega y coordina los subagentes.

## Instalar Jarvis

Requiere Python 3.9 o posterior y una copia de esta rama del repositorio.
Agregar una vez la carpeta de Vengadores al `PATH` en la configuración de la
terminal (por ejemplo, `.bashrc` o `.zshrc`), usando su ubicación real:

```bash
export PATH="/ruta/Vengadores:$PATH"
```

Después, desde el proyecto donde querés usarlo:

```bash
vengadores unidos --host codex --activate
```

El ejemplo instala y activa Jarvis para Codex. Para instalar en OpenCode:
`vengadores unidos` y seleccionar su agente primario Jarvis.
Para Codex: `vengadores unidos --host codex --activate`. Para elegir otro destino:
`vengadores unidos --project /ruta/proyecto`.
`--activate` agrega instrucciones ROOT para Jarvis principal en la raíz elegida.
Repetir instalación y activación en cada worktree; el checkout principal no los
cubre. En cada inicio/recuperación: `vengadores check --project /ruta/worktree`.
Reabrir la sesión del host para cargar instrucciones: un chequeo correcto no
acredita que una conversación ya abierta las haya recargado.

Invocación: **«Usá Jarvis para coordinar esta tarea: <objetivo>»**.
Jarvis PRINCIPAL es el único decisor de coordinación y permanece como supervisor de esa sesión: recibe pedidos, delega, atiende
resultados y vuelve a esperar al usuario. Terminar una tarea no lo detiene.
Podés pedirle «Jarvis, estado», «pausá», «continuá» o «detenete».
La escucha permanece dentro del host; no es un daemon externo.
Ver [supervisión de sesión](skills/jarvis/references/supervision.md).

Se instalan tres skills separadas: `jarvis`, `delegacion-vengadores` y `nick-fury`, vinculadas
automáticamente. Para usar otra skill compatible, agregar
`--delegation-skill /ruta/real/delegacion/SKILL.md`; se referencia sin copiarla.
OpenCode recibe un agente primario `jarvis`, con escritura y shell denegados
al coordinador, y el subagente autor `nick-fury`. Seleccionarlo en la interfaz y pedir la tarea a Jarvis.
El chequeo estructural no acredita subagentes ejecutados: la primera tarea debe
confirmar la interfaz real del host y recibir un ID y una respuesta de agente.

## Documentación

- [Skill de Jarvis](skills/jarvis/SKILL.md)
- [Skill de delegación](skills/delegacion-vengadores/SKILL.md)
- [Nick Fury, creador de skills y subagentes](skills/nick-fury/SKILL.md)
- [Investigación de tokens, idioma y formato](docs/investigacion-skills.md)
- [Contrato operativo](skills/jarvis/references/contract.md)
- [Flujo y controles](skills/jarvis/references/flow.md)
- [Roles de los agentes](skills/jarvis/references/roles.md)
- [Reglas y memoria](docs/memoria.md)
- [Adopción y vinculación](docs/adopcion.md)
- [Resultados y límites de validación](docs/validacion-jarvis.md)
- [Aprendizajes de orquestación](docs/aprendizajes-orquestacion.md)
- [Configuración del proyecto](templates/project/vengadores.yaml)
- [Contrato de una tarea](templates/task/tarea.md)

## Estado

Jarvis tiene una skill, un instalador y un chequeo de dependencias. La ejecución
real usa la skill de delegación incluida y las herramientas/permisos de cada host.
La infraestructura cloud, el servicio de grafo y los deploys no se provisionan con
el instalador. Los subagentes aplican las reglas del proyecto destino y trabajan
con OpenCode según su configuración. No requiere un framework de agentes nuevo.

Cada proyecto conserva su código, memorias, reglas y artefactos. Vengadores guarda
métodos reutilizables. Elegir una revisión de Vengadores y actualizarla de forma
explícita; no cambiar la versión durante una tarea en curso.

Repositorio: [mangellopezdeblasis/Vengadores](https://github.com/mangellopezdeblasis/Vengadores).
No se eligió una licencia de distribución todavía.

Jarvis llama automáticamente a Nick Fury cuando el pedido requiere crear o modificar
una skill o definición de agente; no hace falta nombrar a Nick Fury. Ejemplo:
«Jarvis, creá una skill para revisar migraciones».
Los núcleos son breves y el detalle se carga por caso. No se promete ahorro de tokens
sin medición del tokenizer y del recorrido. Actualizar instalaciones previas con
`vengadores unidos --replace`, que reemplaza las skills distribuidas.

El contador opcional se instala en el entorno Python del worker que ejecuta Nick Fury,
no en GitHub. Ver [medición local y consumo real](skills/nick-fury/references/tokens.md#dónde-instalar-el-contador).

## Perfiles por subagente y escalada

`vengadores unidos` instala también `escalacion-vengadores`, separada de Jarvis
y delegación. Cada rol tiene preferencias iniciales de capacidad y esfuerzo sin
fijar proveedor ni modelo. Jarvis enruta primero la causa del bloqueo y solicita
una mejora solo con justificación técnica, dentro del presupuesto de la tarea.
Ver [política, perfiles, límites y ejemplos](docs/escalada.md).

Para actualizar instalaciones existentes: `vengadores unidos --replace` (reemplaza
las skills distribuidas; conservar antes las personalizaciones). El instalador
comprueba archivos; la aplicación efectiva del perfil depende de controles reales
del host. No se instala un router universal de modelos ni se configuran credenciales.
