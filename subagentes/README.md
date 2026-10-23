# Catálogo de subagentes

Cada carpeta mantiene la identidad y el alcance de un especialista. Jarvis es el
coordinador principal y permanece en [skills/jarvis](../skills/jarvis/SKILL.md);
no hay un worker Jarvis en este catálogo. Las responsabilidades canónicas viven en
[contratos de roles](../skills/jarvis/references/roles.md).

## Identidades y habilidades

- [Nick Fury](nick-fury/SKILL.md) (`nick-fury`): [Autoría de capacidades](nick-fury/habilidades/autoria/SKILL.md).
- [Ant-Man](ant-man/SKILL.md) (`ant-man`): [Preparación de contexto](ant-man/habilidades/contexto/SKILL.md), [Mapa de impacto](ant-man/habilidades/impacto/SKILL.md).
- [Spider-Man](spider-man/SKILL.md) (`spider-man`): [Diagnóstico verificable](spider-man/habilidades/diagnostico/SKILL.md).
- [Capitán América](capitan-america/SKILL.md) (`capitan-america`): [Especificación de comportamiento](capitan-america/habilidades/especificacion/SKILL.md).
- [Vision](vision/SKILL.md) (`vision`): [Plan técnico](vision/habilidades/plan-tecnico/SKILL.md).
- [Thor](thor/SKILL.md) (`thor`): [Implementación asignada](thor/habilidades/implementacion/SKILL.md), [Integración candidata](thor/habilidades/integracion-candidata/SKILL.md).
- [Viuda Negra](viuda-negra/SKILL.md) (`viuda-negra`): [Revisión de conformidad](viuda-negra/habilidades/conformidad/SKILL.md).
- [Hulk](hulk/SKILL.md) (`hulk`): [Análisis adversarial](hulk/habilidades/analisis-adversarial/SKILL.md).
- [Guardianes de la Galaxia](guardianes-de-la-galaxia/SKILL.md) (`guardianes-de-la-galaxia`): [Aceptación E2E](guardianes-de-la-galaxia/habilidades/aceptacion-e2e/SKILL.md).
- [Pantera Negra](pantera-negra/SKILL.md) (`pantera-negra`): [Curación de aprendizajes](pantera-negra/habilidades/aprendizajes/SKILL.md).
- [Soldado del Invierno](soldado-del-invierno/SKILL.md) (`soldado-del-invierno`): [Integración y entrega verificada](soldado-del-invierno/habilidades/entrega/SKILL.md).

## Carga y extensión

1. Jarvis asigna un rol, tarea, revisión, alcance, reglas esenciales y referencias del
   cliente. El agente lee su `SKILL.md` general y únicamente la habilidad necesaria.
2. Para una capacidad nueva del mismo rol, agregá
   `<rol>/habilidades/<habilidad>/SKILL.md` con `name` igual a la carpeta y una
   descripción que indique cuándo usarla. Definí el método y su salida sin repetir
   identidad ni responsabilidades del general.
3. Agregá al general un enlace directo con disparador. Si la capacidad exige otro
   rol o tarea, devolvé la necesidad a Jarvis; no cambies la identidad del worker.
4. Auditá frontmatter, enlaces y límites. Validar documentos no confirma ejecución
   real: el adaptador del host necesita su propia prueba.

Los enlaces relativos presuponen la distribución conjunta de `subagentes/`,
`skills/` y las fuentes compartidas usadas en `docs/`. El instalador debe conservar
esa relación o adaptar referencias y dependencias explícitamente. Nick Fury remite
a su skill de autoría compartida; Pantera y Ant-Man remiten a la política de memoria.
Las reglas, infraestructura, grafo y credenciales del cliente se consultan desde su
proyecto; no se copian a este catálogo.

Estos archivos son instrucciones portables, no un registro automático de agentes
del host. Crean capacidades documentadas; lanzar procesos, configurar perfiles o
permisos y demostrar ejecución sigue correspondiendo al adaptador real y a la
delegación vinculada en `.vengadores/jarvis.json`. Los perfiles se resuelven por
la skill de escalación vinculada, sin fijar modelos en cada identidad.

La estructura permite seleccionar contexto según necesidad. El consumo de tokens
y cualquier ahorro requieren medición real; este catálogo no declara ahorros.
