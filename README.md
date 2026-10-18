# Vengadores

Software Factory Agentic coordinada por **Jarvis**, distribuido como una skill
instalable para OpenCode o Codex. Jarvis solo delega y coordina los subagentes.

## Instalar Jarvis

Requiere Python 3.9 o posterior y una copia de esta rama del repositorio.
Desde la raíz de Vengadores:

```bash
python3 scripts/configure_jarvis.py install --project /ruta/proyecto --host opencode
python3 scripts/configure_jarvis.py check --project /ruta/proyecto
```

Para Codex, cambiar a `--host codex`. La instalación queda en
`.opencode/skills/jarvis` o `.agents/skills/jarvis`, dentro del proyecto destino.
Reabrir la sesión del host para que descubra la skill.

Invocación: **«Usá Jarvis para coordinar esta tarea: <objetivo>»**.

Se instalan dos skills separadas: `jarvis` y `delegacion-vengadores`, vinculadas
automáticamente. Para usar otra skill compatible, agregar
`--delegation-skill /ruta/real/delegacion/SKILL.md`; se referencia sin copiarla.
OpenCode recibe además un agente primario `jarvis`, con escritura y shell denegados
al coordinador. Seleccionarlo en la interfaz y pedir la tarea a Jarvis.
El chequeo estructural no acredita subagentes ejecutados: la primera tarea debe
confirmar la interfaz real del host y recibir un ID y una respuesta de agente.

## Documentación

- [Skill de Jarvis](skills/jarvis/SKILL.md)
- [Skill de delegación](skills/delegacion-vengadores/SKILL.md)
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
