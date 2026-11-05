# Loki — sencillo

Usar solo con objetivo claro, alcance acotado, solución definida, bajo riesgo y
entradas/contexto ya disponibles. Dependencias, contratos y efectos deben ser
conocidos; contar líneas no determina sencillez.

Secuencia exclusiva: **Jarvis → Thor → Jarvis**.

1. Jarvis registra flujo, motivos y condición de escalación según el
   [selector](../skills/jarvis/references/flow.md#selección-de-flujo); entrega a
   Thor tarea, versión, archivos propios, solución, aceptación y contexto disponible.
   Antes de ejecutarlo, exige el [perfil inicial económico obligatorio de Thor](../skills/escalacion-vengadores/references/policy.md#perfil-inicial-obligatorio-de-thor-en-loki):
   `basico/bajo`, traducido a un modelo permitido de menor consumo y coste que el
   perfil normal del destino y su esfuerzo nativo mínimo soportado. Prevalece
   sobre el default de Thor. Sin selección y confirmación real del host, bloquea;
   no hereda silenciosamente un modelo caro. Rige en Codex y Claude con adaptador
   soportado, sin cambiar de proveedor ni pedir otra autorización por este perfil.
2. Thor implementa dentro del alcance y devuelve cambios, revisión, comprobaciones
   realizadas y límites. Aplica las verificaciones proporcionales exigidas por el
   destino/encargo; un control sin ejecutar queda pendiente o no aplica con motivo,
   nunca aprobado.
3. Jarvis registra el resultado y comunica evidencia y pendientes al usuario.

Si faltan datos, aparece una causa desconocida, se amplía el alcance o cambian
riesgo/dependencias, Thor informa y no amplía su tarea. Jarvis reclasifica a Ultron
o Thanos antes de convocar otros roles; no investiga ni agrega fases a Loki.
Si hace falta mayor capacidad, Jarvis reclasifica antes de un upgrade y conserva
los saldos globales de la tarea raíz.
Si el destino exige otros roles o controles incompatibles, también reclasifica.
Deploy, migraciones y escrituras externas no se autorizan por elegir este flujo.
