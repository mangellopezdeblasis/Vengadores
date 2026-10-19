# Contexto mínimo y medición

## Política local de Vengadores

Estas metas son decisiones de diseño revisables, no límites del estándar:

- Descripción orientativa de hasta 240 caracteres; máximo estándar 1024.
- Núcleo orientativo de hasta 250 palabras y 45 líneas; si se mide, apuntar a menos
  de 600 tokens de cuerpo. Son unidades distintas, no conversiones entre sí.
- Conservar restricciones esenciales aunque se supere una meta; justificar la
  excepción y mover solo detalles condicionales a referencias.
- Cargar únicamente la referencia que corresponde al caso. Trasladar texto y luego
  leer todos los anexos no demuestra ahorro.

## Lenguaje, idioma y formato

Usar verbos concretos, términos consistentes y frases completas breves. Quitar
introducciones, reiteraciones y ejemplos redundantes. Evitar abreviaturas crípticas
que produzcan ambigüedad o reintentos. Un ejemplo representativo puede ser más útil
que varias explicaciones.

Español por defecto para este equipo. Conservar nombres de herramientas, claves y
rutas. No duplicar instrucciones en español e inglés. Comparar ambos idiomas solo
con el tokenizer/modelo objetivo y tareas semánticamente equivalentes; no existe
un ganador universal demostrado por esta investigación.

YAML para los metadatos requeridos; Markdown para procedimientos. Usar JSON cuando
una herramienta necesite un esquema y XML cuando la delimitación aporte claridad.
No envolver toda la skill en JSON/XML ni quitar separadores útiles por un supuesto
ahorro. Validar formato, comprensión y errores además del conteo.

## Qué medir

Registrar tokenizer/encoding, revisión y escenario. Contar por separado metadatos,
núcleo, referencias realmente cargadas, esquemas de herramientas, traspasos,
respuestas y reintentos. Registrar tokens de entrada/salida y caché desde el host
cuando estén disponibles; los conteos de archivos no incluyen esos envoltorios.

`python3 scripts/audit.py <skill>` devuelve bytes/palabras/líneas y tokens null:
no convierte caracteres a tokens. Con `--encoding <encoding-real>` puede contar
texto mediante tiktoken instalado por separado; usar un encoding confirmado y
tener presente que su descarga inicial puede requerir red. No mide otros proveedores.
Sin librería o encoding válido, no entrega una cifra inventada.

El ahorro aceptable mantiene o mejora cumplimiento y tasa de errores en casos
comparables. No usar solo el tamaño en disco como criterio de aceptación.

## Fuentes primarias

- [Agent Skills](https://agentskills.io/specification): estructura y carga progresiva.
- [Anthropic](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices): concisión y evaluación por modelo.
- [Codex](https://developers.openai.com/codex/skills/): selección y carga de skills.
- [OpenCode](https://opencode.ai/docs/skills/): descubrimiento por host.
- [OpenAI](https://help.openai.com/en/articles/4936856-understanding-and-counting-tokens): tokens e idiomas.
- [Cookbook](https://developers.openai.com/cookbook/examples/how_to_count_tokens_with_tiktoken): conteo por encoding.

Consulta: 18 de octubre de 2026. No se midieron ahorros de tokens ni calidad entre
idiomas o formatos: tiktoken no estaba instalado. Las metas anteriores deben
evaluarse con datos del uso real.

## Dónde instalar el contador

Tiktoken es opcional y se instala en el mismo entorno Python donde se ejecuta
el auditor de Nick Fury: la máquina local, contenedor o runner cloud del proyecto.
No se instala en GitHub por guardar allí el repositorio. Si se usa un virtualenv,
instalar y ejecutar el auditor con su mismo intérprete:

```bash
python3 -m pip install tiktoken
```

Para runners efímeros, declarar esta dependencia opcional en su imagen o setup.
La primera carga de un encoding puede requerir red; no volver a instalar en cada
llamada de Jarvis. El coordinador no ejecuta mediciones: las delega a Nick Fury.

Seleccionar el encoding confirmado del modelo OpenAI antes de pasar `--encoding`
al auditor. Con Claude, usar su [API de conteo](https://platform.claude.com/docs/en/build-with-claude/token-counting)
y el uso real informado por el proveedor; no presentar un conteo tiktoken como si
fuera el suyo. Para otros modelos, usar su tokenizer o contador oficial.

Un archivo contado antes de la llamada mide contexto estático. Para consumo real,
consultar usage de las respuestas: entrada, salida, caché y razonamiento cuando
el proveedor los expone. Un archivo corto no incluye el resto del historial o las
herramientas. [Referencia OpenAI](https://help.openai.com/en/articles/4936856-understanding-and-counting-tokens).

El inglés puede producir un conteo menor para instrucciones equivalentes en algunos
encodings. Si el contador está disponible, Nick Fury compara ES/EN y conserva la
variante con menor conteo únicamente si mantiene el contrato y supera los mismos
casos de comportamiento. No duplicar ambas variantes en el contexto. Sin medición,
seguir el idioma del equipo y no anunciar un ahorro.
