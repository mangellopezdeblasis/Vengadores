# Delegación de Vengadores

Esta skill es el mecanismo de delegación. Jarvis define el flujo y los especialistas
hacen el trabajo. No reemplaces una llamada real con una conversación imaginaria,
un bloque de texto o la ejecución directa del trabajo del especialista.

## Selección de adaptador

Leé `.vengadores/jarvis.json` para el host configurado y la referencia pertinente:

- Codex con herramientas `collaboration`: `codex.md`.
- OpenCode con herramienta nativa `task`: `opencode.md`.

La presencia real de herramientas y las reglas de la sesión prevalecen sobre el
nombre del host. Si no está el adaptador configurado, informá `bloqueado` y qué
falta. No cambies de proveedor, host o mecanismo silenciosamente. Una denegación de
permisos se conserva como bloqueo; la delegación no amplía autorizaciones.

## Contrato de entrada

Exigí ID de ejecución/tarea, rol, objetivo, alcance, exclusiones, referencias de
entrada, revisión esperada, entregable y criterio de aceptación. Incluí dependencias,
política de datos, límites y, para tareas que escriben, rama/worktree y propiedad de
archivos/recursos. El bootstrap que obtiene esas revisiones es una tarea explícita
de Ant-Man; no inventes SHA, fuentes o resultados faltantes.

Una sesión tiene un rol y tarea fijos, incluso después de completarse o quedar
inactiva. Rechazá un encargo con varios roles: diagnóstico, especificación, plan y
ejecución se asignan a sus especialistas. Jarvis PRINCIPAL conserva las decisiones
de coordinación. No recuperar el supervisor creando un worker Jarvis.

El prompt autosuficiente al agente debe indicar:

1. Su rol y la tarea concreta, con los límites y autorizaciones recibidos.
2. Las instrucciones locales esenciales aplicables, más rutas/referencias de
   consulta, fuentes canónicas y sus versiones/hashes. No omitir reglas obligatorias.
3. Que debe devolver estado, revisión, evidencia, incertidumbres y próxima acción.
4. Que debe conservar su rol y tarea, sin asumir Jarvis ni volver a delegar el
   flujo. Thor ejecuta el encargo; la clasificación y routing vuelven a Jarvis.
5. Que la memoria histórica genera hipótesis; el agente verifica el estado actual.

Codex siempre inicia con `fork_turns: "none"`: nunca heredar historia, logs,
secretos ni contexto de otra tarea. La selección conserva las fuentes autorizadas
y reglas de seguridad. Para corregir el mismo encargo, enviar delta, motivo y
referencias afectadas; no releer documentos completos sin un cambio o necesidad
concreta. Para otro rol/tarea, crear worker nuevo con traspaso de estado, versión,
artefactos y recursos pendientes, sin copiar la conversación.

## Registro y adaptador

Antes de spawn y antes de followup, aplicar el [registro](registry.md). Registrar
la preparación no demuestra que se lanzó un worker: vincular únicamente el ID real
devuelto por la herramienta. Un error se conserva como bloqueo o fallo, nunca como
llamada aceptada. Este guard valida el registro; no impide llamadas directas fuera
del adaptador ni crea permisos del modelo.

## Ejecución y concurrencia

Usá el adaptador del host para iniciar una sesión hija y conservá su ID real. No
registres `en_curso` sin una aceptación real ni `completado` sin su respuesta final.
Para trabajo independiente, iniciá los agentes antes de esperar, dentro del límite
de concurrencia. Para trabajo dependiente, esperá el artefacto y pasalo al siguiente.
Esperá con el mecanismo nativo; no hagas polling de archivos ni esperas de shell.

Un worker que modifica código necesita un worktree propio. Si falta preparación,
delegá primero a un Thor preparador la creación secuencial de ramas/worktrees y
la comprobación de cambios preexistentes. Luego entregá cada ruta a su ejecutor.
Cada worker usa su worktree como directorio y rutas de edición; nunca escribe en
el checkout compartido. El coordinador no crea worktrees ni ejecuta comandos Git.

Los agentes nativos pueden compartir máquina, credenciales, servicios y base de
datos. Un worktree aísla archivos de trabajo, no es un sandbox. No declares ese
aislamiento sin evidencia del proveedor. Respetá la serialización de recursos
compartidos recomendada por Vision y decidida por Jarvis según restricciones;
si es obligatoria una capacidad ausente, bloqueá.

## Respuesta y seguimiento

Relacioná el identificador real con el ID lógico de tarea y mantené estas referencias
en el registro de coordinación o la conversación. Campos mínimos de respuesta:

```json
{
  "worker_id": "ID real del host, vinculado por Jarvis",
  "task_id": "ID lógico recibido",
  "role": "rol asignado",
  "state": "completado | fallido | bloqueado",
  "revision": "SHA/version verificado o null con motivo",
  "result": "resultado breve del especialista",
  "evidence": ["referencias verificables"],
  "need": null,
  "next_action": "acción o null"
}
```

El ID de sesión viene del host, no de un valor inventado por el worker. Si faltan
campos, pedí completarlos en la misma sesión con rol y tarea verificados. Reanudá
solo para continuar o corregir ese encargo, validando antes el registro. Conservá
los informes anteriores. Limitá intentos y
profundidad según configuración. Un timeout o interrupción deja resultado pendiente
o bloqueado, nunca aprobado. Si el host no permite cancelar, informá ese límite.

El recibo es la entrada habitual de Jarvis: ID real, tarea, rol, estado, versión,
resultado breve, referencias de evidencia, `need` y próxima acción. Fuentes,
incertidumbres, trazas y detalles extensos van en el artefacto referenciado; Jarvis
lo consulta según relevancia. No pegar logs completos ni grandes informes en el
contexto principal salvo extracción imprescindible. El recibo de capacidad de la
sección final puede guardarse como evidencia vinculada sin perder sus campos.

## Comprobación real

Antes de afirmar que una instalación funciona, delegá una tarea inocua de lectura:
leer este contrato y devolver un recibo estructurado sin editar archivos, ejecutar
tests, consultar credenciales ni volver a delegar. Registrá el ID emitido por el
host, el recibo final y el adaptador usado. Esta prueba acredita solo ese adaptador
y ese entorno; no valida worktrees, ejecución paralela, grafo, E2E ni deploy.

## Recibo de capacidad y necesidad de escalada

Cada llamada agrega el perfil por rol y el presupuesto restante según
`escalation_skill`; la política y perfiles son canónicos en esa skill separada.
El recibo conserva perfil solicitado, modelo/esfuerzo solicitado y efectivo,
evidencia del host, limitaciones, uso/costo o null si no se exponen.
El worker devuelve `need`: tipo (contexto, ambiguedad, evidencia, herramientas,
permisos, razonamiento o desconocido), motivo, evidencias, intentos, referencias
faltantes y capacidad solicitada; null si no necesita intervención.
Jarvis comprueba campos y enruta; no valida técnicamente la justificación.
