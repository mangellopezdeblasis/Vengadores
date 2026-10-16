# Aprendizajes para coordinar agentes de software

**Documento de análisis documental. Corte: 16 de octubre de 2026.**

Este documento reúne conclusiones reutilizables de cuatro fuentes: observaciones de memoria de trabajo, memorias de Codex, skills de un proyecto de software con varios repositorios y materiales de un equipo de agentes. Separa patrones observados de propuestas para Vengadores. No afirma que exista un runtime, un mecanismo automático de selección de contexto ni coordinación de agentes ya implementados.

Las fuentes de memoria son registros operativos, no un conjunto estadístico controlado. Una observación repetida puede describir el mismo episodio; por eso no se cuentan menciones como incidentes independientes ni se atribuyen tasas de recurrencia.

## 1. Memoria de trabajo tipo Engram

### Qué aporta

Los registros episódicos ayudan a recuperar diagnósticos y errores que no aparecen en la documentación normativa: qué se comprobó, en qué contexto, con qué resultado y qué quedó pendiente. El registro es evidencia histórica útil para generar hipótesis; antes de usarlo como estado actual hay que volver a comprobar el sistema.

### Patrones que conviene convertir en reglas generales

1. **Fijar la revisión y el contrato antes de delegar.** Indicar commit o versión, rutas bajo alcance, comportamiento esperado, límites y consumidores. Un recuerdo o un plan anterior no reemplaza el contrato vigente.
2. **Comprobar qué proceso está sirviendo realmente.** Distinguir código fuente, artefacto compilado, proceso activo y dependencia disponible. Un cambio en disco no demuestra que la aplicación lo esté ejecutando.
3. **Asignar propiedad de archivos y recursos compartidos.** La concurrencia sobre archivos, datos de prueba, procesos, puertos o entornos puede producir interferencia aunque cada agente tenga un checkout distinto.
4. **Clasificar el fallo antes de corregirlo.** Separar problemas del entorno, datos de prueba, producto, contrato y evidencia. Una prueba bloqueada por configuración no demuestra por sí sola un defecto de producto.
5. **Vincular cada afirmación con la evidencia adecuada.** Una respuesta simulada no prueba persistencia; un control visible no prueba que su acción funcione; un test verde no demuestra permisos o despliegue correcto.
6. **Seguir el permiso de extremo a extremo.** Revisar la entrada del usuario, la carga inicial, la acción, el servicio y la autorización final, tanto en el caso permitido como en el denegado.
7. **Preservar configuración y datos locales.** Los archivos de entorno y la configuración específica pueden ser parte necesaria del escenario. Diagnosticar su origen y evitar sustituirlos por valores supuestos.
8. **Modelar compensación en operaciones distribuidas.** Si una operación modifica varios sistemas, explicitar propiedad de datos, orden, fallos parciales, idempotencia y compensación posible.
9. **Respetar el historial de migraciones aplicadas.** En sistemas que versionan migraciones, una corrección suele requerir una migración nueva compatible, no reescribir silenciosamente una ya aplicada.
10. **Probar comportamiento estable, con reintentos acotados.** Las pruebas deben comprobar resultados observables, no detalles frágiles como un número accidental de llamadas. Registrar la causa de cada reintento y detenerse ante un bloqueo persistente.

### Aplicación a Hulk

Hulk puede revisar y reproducir escenarios de riesgo, informar evidencia y señalar brechas. La corrección debe quedar asignada a un agente implementador con propiedad explícita. El informe de Hulk debe distinguir `verificado`, `no aplica`, `parcial` y `pendiente`, e identificar tarea, revisión examinada, comando o escenario, resultado y evidencia. Una lista completa de comprobaciones no certifica por sí sola que el resultado sea correcto.

## 2. Memoria de Codex y delegación

### Lecciones reutilizables

- **No confundir aceptación de una delegación con su ejecución.** Registrar quién la tomó, resultado, estado, evidencia y responsable de integración.
- **Mantener el alcance y los hallazgos accionables.** Pedir rutas, líneas, pasos de reproducción y resultado observado. Resumir primero; incluir detalles completos solo cuando hagan falta para corregir o auditar.
- **Preservar el trabajo existente.** Antes de editar, revisar el estado local relacionado, cambios en curso y errores recientes pertinentes. No descartar cambios ajenos.
- **Separar resultado de integración.** Un agente puede terminar su tarea mientras la integración, la ejecución en el proceso real o la validación final siguen pendientes.
- **Controlar la recursión y el costo de contexto.** Registrar origen y dependencias de delegaciones, limitar la profundidad y no volver a delegar circularmente al agente que originó la tarea.
- **Seleccionar agentes por capacidad y política de datos.** Enviar el contexto mínimo pertinente y respetar las reglas del proyecto destino. La delegación no amplía permisos ni autoriza a mover información sensible a otro proveedor.
- **Usar versiones de fuente, no nombres vagos.** Al reportar, indicar revisión o SHA, rutas y si el árbol tenía cambios locales. Esto facilita reproducir la revisión y detectar resultados obsoletos.
- **Medir antes de declarar ahorro.** Menos texto no siempre significa menos tokens o menor costo: la carga de herramientas, el contexto heredado, los reintentos y la síntesis también cuentan.

### Coordinación simultánea

La simultaneidad es útil cuando se lanzan primero tareas independientes, cada una con entrada, salida y propiedad delimitadas. El orquestador puede esperar a varios resultados y sintetizarlos; los agentes no necesitan escribirse entre sí. Cuando existe una dependencia, se espera el artefacto requerido y luego se inicia la tarea siguiente.

Antes de ejecutar en paralelo, identificar archivos y recursos compartidos. Ramas o worktrees separan algunos cambios de Git, pero no aíslan servicios, bases de datos, puertos, credenciales ni datos externos. Si hay solapamiento, dividir por propiedad, establecer un contrato compartido o serializar esa parte.

## 3. Skills de un proyecto con varios repositorios

### Lo que conviene tomar

- Un punto de entrada central identifica el rol o flujo pertinente, mientras la fuente canónica conserva el detalle.
- Las instrucciones del repositorio destino prevalecen para su código, convenciones, contratos, comandos, seguridad y permisos.
- Los patrones visuales o técnicos se consultan cerca del subrepositorio propietario; la existencia de un directorio anidado no demuestra que sea un submódulo ni que herede reglas automáticamente.
- Los wrappers por herramienta deberían ser delgados y apuntar a instrucciones compartidas para evitar copias divergentes.
- Los flujos de QA separan creación, ejecución y mantenimiento de pruebas; los resultados fallidos deben incluir ambiente, comando, salida y clasificación.
- Los datos compartidos de autenticación o estado pueden exigir serializar pruebas aunque los archivos de prueba sean distintos.
- Las reglas locales y los detalles de negocio se quedan en el proyecto que los conoce. El orquestador guarda el método general y obtiene el contexto específico desde la configuración del destino.

### Límites observados

Una skill que describe un permiso no impone por sí misma ese permiso. Las afirmaciones de solo lectura deben comprobarse frente a las herramientas realmente disponibles. De igual modo, un procedimiento que arranca servicios o crea usuarios necesita declarar el entorno, los efectos, la limpieza y el límite de autorización.

Los comandos, puertos, versiones, nombres de roles, contratos y herramientas cambian entre proyectos. Deben declararse como datos del proyecto y validarse antes de reutilizarlos; no pertenecen a una regla general global.

## 4. Skill de orquestación SDD y equipo del ZIP

### SDD: estructura de fases

El flujo estudiado separa exploración, propuesta, especificación, diseño, tareas, implementación, verificación y archivo. La propuesta precede a especificación y diseño; una vez fijada, estas dos actividades pueden ejecutarse en paralelo si no dependen de decisiones compartidas. Las tareas necesitan ambos resultados; la implementación depende de las tareas y la verificación de una implementación disponible.

Una interfaz escrita para un proveedor concreto no es una garantía portable de ejecución. La capa de orquestación debe describir capacidades requeridas y mapearlas al mecanismo real de cada host. Si el mecanismo no existe, registrar el bloqueo en vez de inventar una API.

El material revisado repetía convenciones entre skill, wrappers y referencias, y contenía rutas y nombres de modelos específicos del entorno. Una mejora propuesta es conservar una fuente canónica y cargar referencias por fase. La reducción de contexto debe medirse en ejecuciones reales; el tamaño de los archivos en disco no equivale a tokens consumidos.

### Equipo de agentes del ZIP

El esquema propone un coordinador central, tareas con contratos explícitos, implementación por capas y revisión/verificación al final. Paraleliza componentes distintos cuando el contrato está estable, y reutiliza al implementador original para corregir hallazgos dentro de un límite de ciclos.

Aspectos transferibles: resumir contratos exactos, identificar dependencias, controlar reintentos y escalar con un traspaso que preserve el diagnóstico. Aspectos que requieren validación: rutas de instalación que no coinciden con los archivos incluidos, herramientas declaradas que no están en el paquete y pasos de verificación que producen efectos secundarios. El stack tecnológico nombrado en el ZIP es propio de ese ejemplo y no debe imponerse a Vengadores.

## 5. Propuestas para Vengadores

Estas propuestas no describen capacidades ya construidas.

1. Mantener un contrato de tarea con objetivo, revisión base, alcance, exclusiones, dependencias, agente responsable, recursos compartidos, entregables y criterio de aceptación.
2. Lanzar en paralelo solo tareas independientes y con propiedad de archivos/recursos explícita. Registrar las dependencias y esperar antes de iniciar etapas dependientes.
3. Identificar el adaptador de delegación disponible por host y verificar inicio, respuesta, cierre y error; no inferir que una instrucción textual ejecutó un agente.
4. En cada traspaso, enviar solo el contexto requerido, enlaces a las fuentes canónicas y un resumen accionable. Adjuntar el informe completo como artefacto cuando sirva para auditoría.
5. Fijar revisión del código y huellas de contexto al iniciar una tarea; invalidar resultados afectados si cambian código, instrucciones o contrato relevante.
6. Mantener separado el conocimiento reutilizable de Vengadores, el conocimiento normativo de cada destino y las notas efímeras de la tarea.
7. Configurar política de datos, permisos, comandos y validaciones en el destino. La configuración debe permitir detectar entradas obligatorias faltantes y no permitir que filtros de rol o presupuesto las oculten.
8. Tratar permisos como una propiedad de toda la cadena y verificar al menos un caso permitido y uno denegado cuando aplique.
9. Reportar cada afirmación de éxito con su evidencia correspondiente; declarar explícitamente cobertura parcial, pendiente o no aplicable.
10. Limitar los reintentos por causa; preservar artefactos, resultados y contexto entre intentos, e indicar cuándo el trabajo necesita decisión humana.
11. Registrar métricas de tokens, latencia, reintentos y calidad por tipo de tarea antes de optimizar prompts, fan-out o cantidad de agentes.
12. Promover una regla general solo cuando incluya evidencia, alcance, excepciones, responsable de mantenimiento y una validación en más de un contexto comparable.

## 6. Límites del estudio

El análisis fue documental. Las memorias reflejan episodios históricos y no se trataron como pruebas del estado actual de los sistemas. El skill de orquestación y el ZIP se inspeccionaron como archivos; no se ejecutaron sus scripts ni se instalaron. El estudio de skills de varios repositorios no valida cada comando, permiso o servicio en runtime. Las propuestas para Vengadores necesitan diseño, revisión y validación antes de convertirse en contratos o automatizaciones.

## 7. Secuencia de trabajo sugerida

1. Acordar el contrato de delegación real y la identidad del orquestador.
2. Definir el esquema mínimo de tarea, handoff, informe y estado.
3. Diseñar el cargador de contexto por destino, acción, rutas y rol, respetando fuentes canónicas y política de datos.
4. Establecer ownership de archivos y recursos compartidos para trabajo concurrente.
5. Validar el flujo con tareas representativas: trabajo pequeño, cambio con dependencias paralelas y fallo de fuente/contexto obligatorio.
6. Medir tokens, latencia, reintentos, reproducibilidad y calidad; ajustar según resultados.

Hasta que esas etapas estén implementadas y medidas, Vengadores sigue siendo un diseño documental para una futura fábrica de software agéntica.
