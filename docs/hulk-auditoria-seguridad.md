# Auditoría de seguridad con Hulk

Esta habilidad adapta una metodología de auditoría a los roles de Vengadores.
Jarvis coordina; los workers Hulk descubren, verifican y redactan. Ant-Man prepara
contexto reutilizable. Los fixes corresponden a Thor, las regresiones a Guardianes
y los aprendizajes a Pantera Negra.

## Instalar

La fuente está en
[la habilidad de Hulk](../subagentes/hulk/habilidades/auditoria-seguridad/SKILL.md).
Su distribución requiere que el catálogo del instalador incluya esta habilidad
junto con `references/` y `upstream/`, sin omitir licencia ni validadores. No copiar
solo el núcleo. Consultá [adopción](adopcion.md) para instalar y preservar una
configuración existente; reabrí la sesión del host después de instalar.

Con Vengadores en PATH, desde el proyecto destino:

```bash
vengadores unidos --host codex --activate
```

Para OpenCode: `vengadores unidos --host opencode`. El catálogo se distribuye en
`.agents/subagentes/` o `.opencode/subagentes/`, respectivamente. Resolvé siempre
`subagents_directory` de `.vengadores/jarvis.json`; la habilidad está en
`<subagents_directory>/hulk/habilidades/auditoria-seguridad/SKILL.md`. No buscarla
como skill separada en `.agents/skills` ni en una carpeta raíz `hulk/`.
Verificá que las referencias upstream existan en ese destino. Para actualizar una
instalación Codex existente: `vengadores unidos --host codex --activate --replace`;
en OpenCode: `vengadores unidos --host opencode --replace`. Guardá personalizaciones
antes de reemplazar archivos distribuidos.
Un catálogo ausente o una instalación incompleta bloquean su uso; no inventar un
comando ni inferir la instalación por encontrar los archivos fuente.

## Pedir una auditoría

Ejemplo: «Jarvis, coordiná con Hulk una auditoría de seguridad en enfoque sobre el
diff y las rutas de autorización del SHA <sha>, cobertura standard. Antes de hunting,
acordá el total de llamadas y reservá verificación y reporte. Entregá findings
confirmados separados de pendientes y registros needs_validation revisados».

Enfoque es el modo por defecto. Para ampliar el objetivo, pedí explícitamente modo
completo e indicá las superficies. quick, standard y deep describen cobertura;
no seleccionan esfuerzo nativo, modelos ni garantizan un número de hallazgos.
La [adaptación](../subagentes/hulk/habilidades/auditoria-seguridad/references/adaptacion.md)
detalla entradas, roles, presupuesto, sandbox y evidencia.

## Qué recibir

Un único reportero técnico escribe el informe en una salida autorizada separada del
código auditado. El informe identifica SHA/snapshot, coverage, fingerprint, evidencia,
validación, exclusiones y pendientes. Los workers descubridor y verificador son
separados; Jarvis no redacta sus conclusiones ni ejecuta tests. Hulk no redelega ni
corrige código.

Las ejecuciones requieren sandbox de SO compatible con upstream. Si el host no lo
confirma, la auditoría se limita a lectura y registra el bloqueo needs_validation:
los candidatos no evaluados quedan en el ledger, fuera de findings.json. Un registro
needs_validation formal requiere revisión independiente de su traza y bloqueo. El resultado de validadores Node es estructural:
no demuestra veracidad. Agotar llamadas o escalada no permite rebajar la evidencia.

El upstream se mantiene fijado al commit
`c1c8a8c1471069fb0e188eeaff69b8e8db6564a8`, preservando su licencia MIT. No se
actualiza, instala dependencias, activa red ni cambia modelos automáticamente.
La instalación no acredita ejecución funcional: el host debe confirmar delegación,
aislamiento, permisos de salida y recibos reales. Código y datos permanecen sujetos
a las restricciones del proyecto y del proveedor autorizado.
