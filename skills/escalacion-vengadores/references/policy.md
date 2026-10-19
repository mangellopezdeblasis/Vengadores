# Política de escalación

## Entradas y destinos

El especialista entrega ID de tarea raíz, versión de las entradas, fallo observado,
evidencia reproducible o referenciada, causa propuesta y siguiente acción. Si la
causa es una hipótesis, debe indicarlo. Jarvis comprueba campos y enruta; la
validez técnica de la recomendación pertenece al especialista.

| Señal informada | Destino y resultado requerido |
| --- | --- |
| Contexto ausente, obsoleto o demasiado amplio | Ant-Man prepara contexto pertinente con fuentes y versión; conserva restricciones esenciales. |
| Comportamiento ambiguo o diagnóstico incompleto | Capitán América y Spider-Man aclaran SDD y diagnóstico; una decisión de producto pendiente vuelve al responsable humano. |
| Capacidad de razonamiento insuficiente | El especialista recomienda un cambio con evidencia del límite y criterio verificable para evaluar el nuevo intento. |
| Evidencia insuficiente para aprobar una afirmación o control | Especialista verificador competente para ese control; entrega evidencia o mantiene el bloqueo. |
| Herramientas o permisos faltantes | Responsable de la capacidad o autorización; bloquear la acción dependiente SIN upgrade ni ampliación de permisos. |
| Causa desconocida | Spider-Man diagnostica antes de recomendar intervención. |
| Defecto de implementación | Especialista responsable del defecto; no justifica automáticamente cambiar el perfil. |

No usar un modelo mayor como sustituto de contexto correcto o una especificación
clara. La solicitud fuera de alcance se devuelve al responsable sin ejecutar
acciones nuevas. Las rutas no conceden permisos ni cambian el contrato de roles.

## Perfiles y capacidades del host

`profiles.json`, distribuido dentro de esta skill, es la fuente portable de
preferencias por rol. Sus claves de rol corresponden al catálogo canónico de
Jarvis. `nivel` admite `basico`, `estandar`, `avanzado`; `esfuerzo` admite `bajo`,
`medio`, `alto`. El JSON tiene exactamente `schema_version: 1` y `roles` en su raíz; cada rol
contiene `nivel` y `esfuerzo`. Son recomendaciones iniciales revisables, sin benchmark ni
promesa de calidad, costo o latencia. No prueban soporte de un host. El riesgo alto documentado por el especialista
puede motivar un perfil inicial avanzado, sujeto a los mismos límites y soporte.

El default efectivo es heredado. Un adaptador solo traduce preferencias mediante
una correspondencia explícita y soportada por su host. No convierte por su cuenta
`avanzado` en un modelo ni `alto` en un parámetro nativo. Si existe una restricción
de modelo fijada por el usuario, debe respetarse.

Registrar la solicitud como opcional u obligatoria y su procedencia. Si falta esa
marca, tratarla como opcional. Soporte desconocido o ausente conserva el heredado
para una solicitud opcional; bloquea únicamente el cambio obligatorio y el trabajo
que dependa de él. Registrar capacidades consultadas, resultado y limitación.
No bloquear tareas independientes por una preferencia opcional no disponible.

Un pedido enviado no acredita aplicación. Registrar `modelo_aplicado` solo con
confirmación del host; en otro caso queda null. Hacer lo mismo con esfuerzo nativo
y perfil efectivo no confirmados, marcando que se conserva el heredado cuando
corresponda. No inventar argumentos de APIs, nombres de modelo ni herramientas.
Los costos estimados o reales desconocidos quedan null. Un límite presupuestario
que exija conocer el costo bloquea el cambio hasta tener información suficiente.

Antes de enviar contexto a otro modelo o proveedor, verificar las restricciones
de datos, residencia, proveedor permitido y presupuesto del destino. No ampliar
permisos, red, credenciales ni acceso a datos para habilitar una escalación.

## Presupuesto único por tarea

Jarvis mantiene el registro real de su sesión, compartido lógicamente por toda
la tarea raíz, con `upgrades_used` y
`retries_used`, ambos inicialmente 0, con `max_upgrades: 1` y `max_retries: 1`. Todos los workers,
subtareas y sesiones de esa tarea consumen ese mismo saldo. No crear otro ID de
tarea para eludirlo. Si el registro se perdió, reconstruirlo de evidencia antes
de continuar; no asumir contadores en cero.

Un upgrade es un intento de elevar nivel, esfuerzo o modelo respecto del efectivo;
una solicitud combinada consume un upgrade. Una configuración inicial confirmada
no consume upgrade; cambiarla después para elevar capacidad sí lo consume. Un retry
es repetir un intento fallido del mismo objetivo en cualquier worker. Una nueva
sesión o un cambio de proveedor no crea otro presupuesto. Un upgrade que exige relanzar el worker consume ambos saldos, aunque el cierre
anterior no sea un fallo. Contar ese relanzamiento una sola vez como retry; la
traducción del adaptador no genera otro retry. Los intentos iniciales normales
de fases distintas no son retries.

Jarvis serializa las solicitudes y registra cada reserva en su registro real de
sesión antes de invocar al adaptador de delegación. No se supone un backend
persistente ni un contador transaccional implementado. No permitir reservas
simultáneas: si la sesión no puede garantizar su serialización o pierde el
registro, bloquear nuevas acciones hasta reconstruirlo con evidencia fiable. Una reserva enviada cuenta aunque
el host rechace el cambio o el intento falle. No hay reposición automática.
Evaluar soporte sin solicitar un cambio no consume el saldo.

Corregir contexto o aclarar el SDD no constituye por sí mismo un upgrade. Volver
a ejecutar el objetivo fallido después de esa corrección sí es retry. La
preparación, el diagnóstico y verificaciones de objetivos nuevos no conceden
reintentos adicionales para el objetivo fallido. Al agotar un saldo, el especialista
entrega evidencia y bloqueo para decisión humana; esta política no autoriza excederlo.

## Esquemas de solicitud y recibo

Estos objetos definen el contrato instruccional; no son parámetros de una API del
host. Las claves son exactas. `task_id` es estable durante toda la tarea raíz;
`global_counters` refleja el registro compartido, no uno nuevo por mensaje. Los
campos de perfil usan `level` y `effort` en los mensajes; se corresponden con
`nivel` y `esfuerzo` del JSON portable sin inferir parámetros nativos.

Solicitud, antes de reservar o ejecutar:

```json
{
  "task_id": "ESC-EJEMPLO-001",
  "worker_id": "worker-origen",
  "role": "thor",
  "revision": null,
  "version_ref": "snapshot-o-hash-de-entradas",
  "cause": "razonamiento",
  "evidence": ["referencia-al-informe-del-especialista"],
  "recommendation": "Cambiar perfil y comprobar el criterio documentado",
  "requested_profile": {"level": "avanzado", "effort": "alto", "model": null},
  "required": false,
  "requirement_source": null,
  "relaunch": false,
  "retry": false,
  "global_counters": {"upgrades_used": 0, "retries_used": 0}
}
```

`cause` admite `contexto`, `ambiguedad`, `evidencia`, `herramientas`, `permisos`,
`razonamiento`, `desconocido` o `defecto`. Corresponde al tipo `need` informado por
el worker; `defecto` permite registrar una causa de implementación ya diagnosticada.
`evidencia` exige especialista verificador; `herramientas` y `permisos` exigen
responsable/bloqueo sin upgrade; `desconocido` se enruta a Spider-Man.
`requested_profile.level` admite los niveles portables o null cuando no se pide
cambio; `requested_profile.effort` admite los esfuerzos portables o null. Un
modelo desconocido queda null. `required: true` exige una fuente explícita en
`requirement_source` y soporte real confirmado antes de cambiar. `relaunch` indica
que el upgrade requiere relanzar; `retry` indica repetición de un fallo. Ambos
verdaderos consumen un solo retry, además del upgrade aplicable.

Recibo, después de reservar y recibir respuesta o de registrar el bloqueo:

```json
{
  "task_id": "ESC-EJEMPLO-001",
  "worker_id": "worker-efectivo",
  "role": "thor",
  "state": "bloqueado",
  "revision": null,
  "version_ref": "snapshot-o-hash-de-entradas",
  "cause": "razonamiento",
  "evidence": ["referencia-al-informe-del-especialista"],
  "recommendation": "Conservar heredado hasta confirmar soporte obligatorio",
  "requested_profile": {"level": "avanzado", "effort": "alto", "model": null},
  "required": true,
  "requirement_source": "referencia-al-requisito",
  "capability": "desconocida",
  "effective_profile": {"mode": "heredado", "level": null, "effort": null, "model": null},
  "host_confirmation": null,
  "cost": null,
  "reservation": {"upgrade": false, "retry": false},
  "global_counters": {"upgrades_used": 0, "retries_used": 0},
  "artifacts": [],
  "uncertainties": ["Soporte del host sin confirmar"],
  "next_action": "Confirmar soporte antes del cambio obligatorio"
}
```

`capability` admite `confirmada`, `no_soportada` o `desconocida`.
`state` admite `completado`, `bloqueado` o `fallido`. `effective_profile.mode`
admite `heredado` o `confirmado`; nivel, esfuerzo nativo y modelo efectivos solo
se completan con confirmación del host. El `effort` solicitado es portable; el
`effort` efectivo es nativo y puede tener otro vocabulario confirmado por el host.
`host_confirmation` es una referencia o null. `cost` es null si se desconoce; si
se conoce, es un objeto con `amount`, `currency`, `kind` (`estimado` o `real`) y
`source`. No deducir precios de perfiles. Cada contador admite solo 0 o 1; las
reservas booleanas indican lo consumido por esta acción, ya incluido en los totales.
`revision` es null sin Git; `version_ref` conserva entonces snapshot o hashes.

## Cambio de sesión y recibo

Si el host requiere un worker nuevo, guardar referencias de artefactos y versión
exacta de las entradas y cambios (SHA si existe; hashes o snapshot si no hay Git).
Pedir el cierre del worker anterior y esperar su confirmación antes de editar con
el reemplazo. Si no se confirma el cierre, bloquear las escrituras. Reanudar con
alcance, propietario de archivos, límites, registro global y referencias conservados;
no copiar historial ni datos innecesarios. Respetar el aislamiento del destino.

El recibo incluye ID de tarea raíz y worker, rol, estado, versión y evidencia del
especialista; causa y recomendación; perfil solicitado, obligatoriedad y origen;
capacidad observada del host; perfil efectivo, modelo y esfuerzo nativo confirmados
o null; costos conocidos o null; reservas y contadores globales; artefactos,
incertidumbres y próxima acción. Jarvis registra el resultado; el especialista
comprueba el criterio de éxito sobre la versión efectiva.

Esta política documenta decisiones. Las reservas dependen del registro real
de sesión y de la serialización de Jarvis; el cierre de workers depende de las
capacidades comprobadas del host. La documentación no implementa persistencia
ni un router autónomo.
