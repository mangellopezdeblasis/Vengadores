---
name: escalacion-vengadores
description: Enruta bloqueos de contexto, ambigüedad o razonamiento y solicitudes de cambio de perfil en tareas delegadas de Vengadores, con límites globales y evidencia del especialista.
---

# Escalación de Vengadores

1. Recibí ID de tarea, versión, evidencia y recomendación del especialista. Jarvis
   solo enruta y registra; no diagnostica ni decide la validez técnica.
2. Para decidir el destino, consultá la [política](references/policy.md): contexto
   a Ant-Man; ambigüedad a SDD/diagnóstico; razonamiento solo con recomendación
   evidenciada. No elevar permisos ni eludir límites de datos o proveedor.
3. Para solicitar un perfil, cargá los [perfiles portables](references/profiles.json).
   Nivel y esfuerzo son preferencias, no modelos ni parámetros nativos universales.
   Conservá el perfil heredado si el host no admite el cambio opcional; soporte
   desconocido bloquea únicamente un cambio obligatorio. Registrá modelo aplicado
   solo cuando el host lo confirme; costos desconocidos quedan null.
4. Usá un registro único por tarea: máximo UN upgrade y UN retry globales,
   compartidos por todos los workers y sesiones. Reservá cada intento antes de
   ejecutarlo; si falta saldo o registro fiable, detené esa acción e informá bloqueo.
5. Si el cambio exige nueva sesión, conservá artefactos y versión y confirmá el
   cierre del worker previo antes de editar. No reinicies los contadores.
6. Entregá perfil solicitado y efectivo, confirmación del host, evidencia,
   contadores globales, incertidumbres y próxima acción. No afirmes ahorro ni
   ejecución funcional a partir de esta política escrita.
