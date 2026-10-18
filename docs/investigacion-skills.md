# Diseño de skills con contexto mínimo

Investigación documental y aplicación a Vengadores. Consulta: 18 de octubre de 2026.
Nick Fury es el autor de skills y contratos de subagentes; Jarvis coordina sus llamadas.

## Hallazgos y aplicación

La [especificación Agent Skills](https://agentskills.io/specification) distingue
metadatos, cuerpo al activar la skill y recursos bajo demanda. Su formato requiere
YAML y Markdown; no define una conversión de caracteres a tokens. La primera
optimización es evitar cargar capacidades y referencias irrelevantes. Las
descripciones deben permitir una selección correcta, sin contener todo el método.

[Anthropic](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
recomienda concisión, evitar conocimiento general repetido y evaluar en los modelos
utilizados. Se adoptan núcleos breves, fuentes canónicas y referencias con condición
explícita de carga. Las restricciones esenciales permanecen en el núcleo: moverlas
a un anexo opcional puede ahorrar texto y empeorar el comportamiento.

Los mecanismos de descubrimiento de [Codex](https://developers.openai.com/codex/skills/)
y [OpenCode](https://opencode.ai/docs/skills/) dependen del host. Un archivo de skill
contiene instrucciones; no crea por sí solo un agente ni impone permisos. Nick Fury
genera el contrato y el perfil que el host soporte, y solicita a Jarvis una llamada
real para validar ejecución. No agrega APIs imaginarias ni modelos fijos por defecto.

## Lenguaje e idioma

La decisión local es español claro, verbos concretos y nombres técnicos originales.
Se evita duplicar traducciones y usar abreviaturas que causen ambigüedad. Una skill
debe añadir decisiones útiles, no una introducción al dominio.

[OpenAI](https://help.openai.com/en/articles/4936856-understanding-and-counting-tokens)
explica que el conteo depende del texto, idioma y tokenización. El
[Cookbook](https://developers.openai.com/cookbook/examples/how_to_count_tokens_with_tiktoken)
muestra el conteo por encoding. No hay una cifra universal de ahorro al pasar de
español a inglés. Para compararlos, conservar instrucciones equivalentes y evaluar
tokenizer/modelo, comprensión, cumplimiento y reintentos. No traducir todo sin esa
comparación ni extrapolar un encoding OpenAI a otro proveedor.

## Formato

| Contenido | Decisión local |
| --- | --- |
| Metadatos | YAML con name y description; campos opcionales solo si hacen falta. |
| Instrucciones | Markdown breve y listas cuando aclaren el procedimiento. |
| Salida para herramientas | JSON cuando exista un esquema o consumidor. |
| Bloques delimitados | XML si ayuda al caso; no imponerlo a todas las skills. |
| Operaciones repetibles | Scripts parametrizados y salida resumida. |

Ninguno de esos formatos se declaró ganador en tokens. La selección prioriza el
contrato del consumidor y la claridad; minificar una instrucción hasta volverla
ambigua puede aumentar el costo total por correcciones.

## Aplicación y límites de medición

La [política canónica de Nick Fury](../skills/nick-fury/references/tokens.md) contiene
metas locales revisables para el núcleo. El auditor comprueba campos mínimos,
referencias y tamaño. Los presupuestos son avisos, no una orden de borrar límites.

En esta revisión las entradas cambiaron así:

| SKILL.md | Bytes UTF-8 antes | Bytes después |
| --- | --- | --- |
| Jarvis | 7322 | 1974 |
| Delegación | 4651 | 1680 |
| Nick Fury, nueva | — | 1653 |

El detalle anterior de Jarvis/delegación se conserva en referencias bajo demanda.
Estas cifras miden archivos, **no tokens ni ahorro de una ejecución**. Si un recorrido
carga todos los anexos puede consumir tanto o más contexto. Se deben incluir también
herramientas, traspasos, resultados y reintentos al medir el uso real.

Tiktoken no estaba instalado; no se midieron tokens ni calidad comparada entre
idiomas/formatos. El auditor entrega tokens null sin medición y permite especificar
un encoding con una instalación de tiktoken disponible. Las pruebas estructurales
no demuestran selección correcta ni calidad: eso requiere casos del host/modelo.
