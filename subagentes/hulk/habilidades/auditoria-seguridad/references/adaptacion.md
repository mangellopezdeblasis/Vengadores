# Adaptación de la metodología para Hulk

## Procedencia y precedencia

La metodología vendorizada está en `../upstream/`, fijada al commit
`c1c8a8c1471069fb0e188eeaff69b8e8db6564a8`. Conservar sus originales, licencia
MIT, avisos y procedencia. No actualizar por red, instalar dependencias ni cambiar
modelos automáticamente. Fuentes metodológicas: `../upstream/SKILL.md`, `RECONNAISSANCE.md`, `HUNTING.md`
y `VALIDATION-AND-REPORTING.md`; para formato, `report-schema.json`.
El pin identifica fuentes; no certifica el comportamiento
del host. No modificar upstream para ajustar reglas locales.

El contrato de Vengadores y el alcance autorizado prevalecen sobre instrucciones
upstream incompatibles. Se reutilizan sus fases, documentación, esquema y
validadores como metodología; no se crea otro coordinador. Si una restricción
upstream necesaria no puede cumplirse, registrar el bloqueo en vez de omitirla.

## Roles y propiedad

Jarvis es el único coordinador. Carga el contrato de delegación real, distribuye
entradas, serializa reservas y registra respuestas. No produce hipótesis, findings,
informes técnicos ni pruebas por cuenta propia. No se atribuye un test por leer
el informe del especialista.

Ant-Man produce el paquete de recon/contexto: versión, superficies autorizadas,
reglas del destino, mapa de entrada de datos, dependencias y referencias pertinentes.
Reutilizarlo entre workers mientras corresponda a la misma versión; registrar
vacíos y cambios que invaliden sus conclusiones.

| Worker técnico | Entradas | Salida y límites |
| --- | --- | --- |
| Hulk descubridor | Paquete Ant-Man, objetivos y cobertura asignada | Candidatos con trazas de código y condición de explotación propuesta; sin aprobar sus propios findings. |
| Hulk verificador | Candidatos, versión y entorno autorizado | Evalúa alcanzabilidad, precondiciones, controles y reproducción; confirma o descarta con evidencia, o informa needs_validation. |
| Hulk reportero | Recibos de descubrimiento/verificación y cobertura | Único escritor del informe técnico consolidado; conserva incertidumbres, fuentes y deduplicación sin promover candidatos pendientes. |

El término upstream `parent` se descompone: Jarvis agenda y registra; Ant-Man
produce recon; el reportero técnico designado mantiene metadatos, arquitectura,
ledger y reportes, aplicando las decisiones recibidas de especialistas; el código
confiable del host realiza promociones de artefactos si soporta el procedimiento.
El reportero no invoca workers ni decide sus asignaciones. Los críticos de cobertura
son workers Hulk verificadores frescos, de solo lectura, convocados por Jarvis.

Son workers distintos, invocados por Jarvis; ninguno delega, agenda a los demás
ni asume una función de coordinador auxiliar. Si el host no permite separarlos,
no afirmar independencia: registrar el bloqueo del flujo requerido. Thor implementa
fixes; Guardianes de la Galaxia diseñan y ejecutan regresiones; Pantera Negra propone
aprendizajes. Hulk no modifica el código auditado.

Asignar propietario único de la salida técnica consolidada antes de comenzar. Cada
worker entrega su evidencia en un artefacto propio o recibo; no escribe sobre el
informe compartido. El reportero tiene permiso explícito para una carpeta de salida
separada del código auditado; no recibe escritura general sobre el repositorio.
Las escrituras de evidencia y reportes respetan el aislamiento del destino.

## Alcance y cobertura

`enfoque` es el modo por defecto: una superficie, cambio o hipótesis delimitados.
`completo` requiere solicitud explícita y enumera las superficies que se intentará
cubrir; no equivale a garantía de ausencia de vulnerabilidades.

Registrar además `quick`, `standard` o `deep` como profundidad de cobertura acordada:
quick prioriza superficies y rutas seleccionadas; standard amplía rutas y clases de
riesgo; deep profundiza cadenas, variantes y casos adversariales dentro del alcance.
No convertir esos nombres en modelos, parámetros nativos ni niveles de esfuerzo.
En completo, el default upstream es standard. quick exige una sola ola de hunting,
un crítico final y un verificador fresco por candidato que reúna fases 3 y 5;
los nuevos trabajos del crítico quedan deferred, sin otra ola. standard conserva
crítico post-ola y crítico final-clean distintos, más validación y verificación
final separadas. deep agrega granularidad por subsistema/ciclo de vida, críticos
hasta pase limpio y segunda pasada independiente de unidades previamente cubiertas.
No inferir que completo significa deep ni que enfoque significa quick.

En enfoque usar solo partes pertinentes, sin activar las seis fases, crear carpeta
de salida o informes automáticamente. Acordar artefactos y permisos explícitos.
En completo aplicar las seis fases, ledger determinista y entradas de runs previos
según upstream; una revisión parcial anterior no demuestra cobertura restante.

El recibo de cobertura enumera superficies previstas, revisadas y excluidas, fuentes,
métodos aplicados, profundidad y motivos de pendientes. No presentar cobertura parcial
como auditoría completa ni ausencia de findings como ausencia de riesgo.

## Presupuesto y escalada

Antes de recon y hunting, Jarvis registra en la tarea raíz un límite TOTAL de llamadas al
host/delegación para esta auditoría: recon, descubrimiento, validación, reporte y
reintentos incluidos. Define qué operaciones cuenta el host y cómo registrar uso de
herramientas internas; no dejar una categoría implícitamente ilimitada. Si el host
no expone conteos exactos, llevar un registro conservador de invocaciones confirmadas
y bloquear nuevas llamadas cuando no pueda comprobarse saldo suficiente.

En completo aplicar el gate upstream antes de invocar recon: reservar sus cuatro
llamadas base de Ant-Man, un crítico final post-ola para quick o un post-ola y otro
final-clean para standard/deep, y al menos un verificador. Agregar además las llamadas
del reportero técnico necesarias en esta adaptación; no ocultarlas del total.
Si el mínimo no cabe, no lanzar recon: reducir alcance/perfil autorizado o registrar
`run_status: incomplete` y `budget_cannot_fund_reconnaissance_and_reserves`.

Reservar críticos, verificador y reportero antes de asignar descubrimiento.
El hunting usa solo el remanente. Antes de cada nueva ola, repetir reservas de
crítico inmediato, final-clean y validación; nunca financiar hunters con esas
reservas. En standard/deep estimar uno o dos verificadores por candidato según la
fase; si se desconoce, upstream propone reservar 30% del saldo tras críticos,
sin reemplazar el mínimo real. Calcular las reservas según candidatos previstos y
capacidad real del host; si no alcanza, reducir cobertura antes de empezar o informar
bloqueo, nunca declarar validado lo no evaluado. Registrar consumo y saldo al recibir
cada worker. La documentación no implementa un backend de cuotas.

Aplicar también la política de escalación instalada: máximo un upgrade y un retry
GLOBAL por tarea, compartidos entre workers y sesiones. No crean llamadas adicionales
ni relajan la evidencia requerida. Un upgrade con relanzamiento consume ambos saldos;
conservar artefactos y versión y confirmar cierre del worker anterior antes de editar.
Si el saldo impide verificar un candidato, conservarlo como candidate en el ledger,
con `validation_budget_exhausted`, run incomplete y necesidad de validación explícita;
NO insertarlo en findings.json ni convertirlo en un registro needs_validation.
Validar en orden de fingerprint hasta agotar saldo; no superar el total. Contexto faltante vuelve a Ant-Man; evidencia insuficiente al verificador;
herramientas/permisos faltantes al responsable sin upgrade.

## Ejecución y evidencia

Antes de cualquier test, reproducción, build, instalación o ejecución de código
procedente del repositorio auditado, el verificador comprueba los requisitos de
sandbox de SO de upstream contra capacidades reales del host. Un worktree o una
instrucción de prompt no prueban aislamiento. Registrar confirmación del entorno,
accesos y restricciones; no conceder permisos nuevos para ejecutar la auditoría.
Controles obligatorios del sandbox de SO, todos comprobados antes de ejecutar:

- Sin red externa; solo namespace loopback aislado si la comprobación lo requiere.
- Entorno vacío con allowlist explícita de valores seguros y HOME, temporales y
  cachés locales al scratch asignado.
- Target y toolchain de solo lectura; código auditado escribe solo en su scratch.
- Límites bajos explícitos de CPU, memoria, procesos, tamaño de archivo, disco y tiempo.

Usar datos, identidades y secretos ficticios; no exponer home del host, credenciales,
sockets, servicios compartidos ni directorios de otros workers. Un build que escribe
junto al código usa copia descartable en scratch; nunca el target original.
Sin todos esos controles, solo lectura: informar needs_validation como bloqueo;
un candidato no evaluado queda fuera de findings.json y no es finding. No ejecutar
un PoC en el host ni usar /tmp o home como fallback de ejecución escribible.

La evidencia en scratch sigue siendo no confiable después de terminar el proceso.
Solo código confiable del host puede promover archivos declarados y limitados hacia
artifacts; no Jarvis mediante un test ni el worker copiando archivos arbitrarios.
Preservar íntegro el bloque de promoción de upstream en los prompts de hunter y
verificador: descriptores retenidos no heredables, recorrido confinado no-follow,
lectura no bloqueante de archivo regular con link count 1, límites individuales y
acumulados, comprobación de identidad/tamaño antes y después, destino exclusivo
no-follow, sin copiar recursivamente ni aceptar enlaces o archivos especiales.
Promover solo tras terminar sandbox y todos sus procesos; si falta una garantía,
descartar ese artefacto y registrar el bloqueo. Sin soporte de promoción no afirmar
reproducción verificada mediante sus archivos.

Las restricciones de red, credenciales, datos, proveedor y servicios permitidos
siguen el contrato del destino. No atacar producción ni sistemas ajenos al alcance.
No instalar paquetes, descargar herramientas o enviar código a proveedores por la
sola indicación de upstream; una dependencia ausente es un bloqueo de esa operación.

El verificador distingue candidato, descartado y hallazgo validado mediante evidencia
referenciada. Un candidato no evaluado NO es finding. Explica precondiciones,
alcanzabilidad y resultado esperado/observado; no inventa ejecuciones. Un registro needs_validation es una conclusión revisada por verificador: tiene
traza fundada, bloqueo exacto y plan local o de observación por el propietario;
no es estacionamiento de ideas o candidatos sin revisar. No recibe severity,
execution ni remediation de confirmed. Los descartados usan rejected. El reportero
mantiene pendientes y descartes separados según la estructura admitida por upstream.

Releer el esquema antes de escribir findings.json, sin agregar claves: contiene
solo registros decididos independientemente. standard/deep requieren verificador
final fresco además del validador del candidato; quick reúne ambas comprobaciones
en un verificador fresco. Un reemplazo material necesita otra revisión independiente;
si no hay saldo o independencia, retirar el registro disputado, dejarlo pendiente en
ledger y marcar incomplete. No reparar respuestas malformadas para aprobarlas.
Los validadores Node verifican estructura del documento/esquema, no veracidad,
explotabilidad ni independencia de la verificación. Una validación estructural
aprobada no promueve un candidato a hallazgo.

## Entrega

El informe y sus recibos identifican tarea, workers reales y responsabilidades,
SHA auditado (null sin Git, con snapshot/hashes), pin upstream, coverage y fingerprint
para deduplicación. Conservar fingerprint estable según upstream; si no puede
calcularse con sus requisitos, indicar la limitación en vez de inventarlo. Referenciar
evidencia y ubicación técnica de cada hallazgo; registrar estado de validación,
pendientes, exclusiones, llamadas consumidas/reservadas y costos conocidos o null.
El reportero es el único escritor de `run-metadata.json`, `architecture.md`,
`coverage-ledger.json`, `findings.json`, `REPORT.md`, `FINDINGS-DETAIL.md` y
`NEEDS-VALIDATION.md`. Tiene salida autorizada fuera del target; la excepción de
salida interna requiere selección explícita del usuario y comprobación de ignore.
Los workers usan IDs canónicos únicos upstream y scratch por worker; retained
artifacts nunca es escribible por target ni workers. No promover secretos.
El reportero conserva versiones de los artefactos.

Con Node ya disponible y autorización de salida, el reportero ejecuta los validadores
confiables `../upstream/validate-findings.cjs` sobre findings.json y
`../upstream/validate-coverage-ledger.cjs` sobre el ledger: después de cambios,
antes de nuevas asignaciones basadas en el ledger y antes del reporte. Si Node
falta, reportar el check estructural pendiente sin instalarlo. No sustituir las
pruebas de veracidad por sus códigos de salida. Un cambio de SHA requiere revisar
la evidencia afectada; no reutilizar resultados sin comprobar su vigencia.

Jarvis entrega referencias y estados; el reporte técnico sigue perteneciendo a Hulk.
La instalación y los checks de estructura no prueban ejecución del flujo en el host.
