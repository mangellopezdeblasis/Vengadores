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
vengadores unidos
```

Instala y vincula Jarvis, delegación y Nick Fury en el directorio actual para OpenCode.
Para Codex: `vengadores unidos --host codex`. Para elegir otro destino:
`vengadores unidos --project /ruta/proyecto`.
Reabrir la sesión del host para que descubra las skills.

Invocación: **«Usá Jarvis para coordinar esta tarea: <objetivo>»**.
Jarvis permanece como supervisor de esa sesión: recibe pedidos, delega, atiende
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

Nick Fury se invoca mediante «Jarvis, pedile a Nick Fury crear una skill para <objetivo>».
Los núcleos son breves y el detalle se carga por caso. No se promete ahorro de tokens
sin medición del tokenizer y del recorrido. Actualizar instalaciones previas con
`vengadores unidos --replace`, que reemplaza las skills distribuidas.
