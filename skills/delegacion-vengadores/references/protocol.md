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

El prompt al agente debe indicar:

1. Su rol y la tarea concreta, con los límites y autorizaciones recibidos.
2. Las instrucciones del proyecto que debe consultar y los artefactos pertinentes.
3. Que debe devolver estado, revisión, evidencia, incertidumbres y próxima acción.
4. Que no debe volver a delegar el flujo ni crear subagentes salvo autorización
   explícita en su contrato. Los resultados vuelven al coordinador.
5. Que la memoria histórica genera hipótesis; el agente verifica el estado actual.

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
compartidos indicada por Vision; si es obligatoria una capacidad ausente, bloqueá.

## Respuesta y seguimiento

Relacioná el identificador real con el ID lógico de tarea y mantené estas referencias
en el registro de coordinación o la conversación. Campos mínimos de respuesta:

```json
{
  "task_id": "ID lógico recibido",
  "role": "rol asignado",
  "state": "completado | fallido | bloqueado",
  "revision": "SHA/version verificado o null con motivo",
  "result": "resultado del especialista",
  "evidence": ["referencias verificables"],
  "uncertainties": [],
  "next_action": "acción o null"
}
```

El ID de sesión viene del host, no de un valor inventado por el worker. Si faltan
campos, pedí completarlos en la misma sesión cuando sea posible. Reanudá al mismo
agente para correcciones y conservá los informes anteriores. Limitá intentos y
profundidad según configuración. Un timeout o interrupción deja resultado pendiente
o bloqueado, nunca aprobado. Si el host no permite cancelar, informá ese límite.

## Comprobación real

Antes de afirmar que una instalación funciona, delegá una tarea inocua de lectura:
leer este contrato y devolver un recibo estructurado sin editar archivos, ejecutar
tests, consultar credenciales ni volver a delegar. Registrá el ID emitido por el
host, el recibo final y el adaptador usado. Esta prueba acredita solo ese adaptador
y ese entorno; no valida worktrees, ejecución paralela, grafo, E2E ni deploy.
