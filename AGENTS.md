# Instrucciones para trabajar en Vengadores

- Jarvis se distribuye como skill instalable en skills/jarvis; la infraestructura cloud, el grafo y los deploys requieren herramientas del destino.
- Mantener Jarvis como orquestador y OpenCode como herramienta prevista.
- Jarvis usa skills/delegacion-vengadores como dependencia separada por defecto. Una skill externa se vincula por referencia. Si faltan herramientas, registrar el bloqueo; no inventar su interfaz.
- Respetar las reglas del proyecto destino y las instrucciones del usuario.
- Cada informe debe identificar tarea, commit, evidencia y resultado.
- No tratar un cambio de documentación como automatización implementada.
- No copiar credenciales, datos privados o reglas específicas de un cliente a la memoria global.
- Pantera distingue conocimiento del destino, de Vengadores y temporal de la tarea.
- Mantener el selector y flujo completo canónicos en skills/jarvis/references/flow.md; villanos/loki.md, ultron.md y thanos.md contienen los recorridos seleccionables. Roles y contrato permanecen en skills/jarvis/references; los otros MD enlazan a estas fuentes. Mantener las plantillas alineadas.


- Aplicar skills/nick-fury para crear o ajustar skills/subagentes: núcleos breves, referencias condicionales, español por defecto y sin ahorros de tokens no medidos.
