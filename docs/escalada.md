# Escalada de tareas delegadas

La skill [escalacion-vengadores](../skills/escalacion-vengadores/SKILL.md) permite
al host seguir una política común ante bloqueos. Jarvis enruta recomendaciones
del especialista y registra estados y evidencia; no realiza el diagnóstico técnico.

## Instalar y usar

Desde el proyecto destino, con Vengadores en el PATH:

```bash
vengadores unidos --host codex
```

Para OpenCode usar `vengadores unidos --host opencode`. El instalador incluye
`escalacion-vengadores` junto a Jarvis y vincula `escalation_skill` en
`.vengadores/jarvis.json`. Reabrí la sesión del host. Para instalaciones existentes,
consultá las reglas de preservación y reemplazo en [adopción](adopcion.md).

Pedí: «Usá Jarvis para coordinar <objetivo>. Ante bloqueos, aplicá la política de
escalación y conservá el mismo ID de tarea». Podés agregar una preferencia inicial
por rol y aclarar si un cambio es obligatorio o solo deseable. Los requisitos
obligatorios deben tener una fuente explícita; no conceden nuevos permisos.

La política es instruccional: el host ejecuta únicamente acciones soportadas. No
instala un router autónomo ni un servicio persistente. Si falta la interfaz de
delegación o una capacidad obligatoria, la acción dependiente queda bloqueada.

## Perfiles iniciales

La fuente portable es [profiles.json](../skills/escalacion-vengadores/references/profiles.json).
Los roles corresponden al [catálogo de Jarvis](../skills/jarvis/references/roles.md).

| Rol | Nivel preferido | Esfuerzo preferido |
| --- | --- | --- |
| Jarvis | basico | bajo |
| Nick Fury | estandar | medio |
| Ant-Man | basico | bajo |
| Spider-Man | estandar | medio |
| Capitán América | estandar | medio |
| Vision | estandar | medio |
| Thor | estandar | medio |
| Viuda Negra | estandar | medio |
| Hulk | avanzado | alto |
| Guardianes de la Galaxia | estandar | medio |
| Pantera Negra | estandar | medio |
| Soldado del Invierno | estandar | medio |

Son preferencias revisables, no nombres de modelos ni esfuerzos nativos universales.
El default efectivo es heredado. El adaptador requiere una correspondencia real y
el host debe confirmar el modelo aplicado. Un cambio opcional sin soporte conserva
el heredado; un cambio obligatorio sin soporte confirmado bloquea su trabajo dependiente.
Modelo, esfuerzo efectivo y costo desconocidos se registran como null. No hay
promesas de ahorro, precio o calidad. Un riesgo alto documentado puede justificar
un perfil inicial avanzado sin cambiar permisos ni restricciones de datos/proveedor.

## Resolver bloqueos

| Necesidad del worker | Ruta |
| --- | --- |
| Contexto | Ant-Man prepara fuentes y versión pertinentes. |
| Ambigüedad | Capitán América y Spider-Man aclaran SDD y diagnóstico. |
| Evidencia insuficiente | Especialista verificador del control afectado. |
| Herramientas o permisos faltantes | Responsable de la capacidad; bloqueo sin upgrade. |
| Causa desconocida | Spider-Man diagnostica. |
| Razonamiento | Recomendación evidenciada del especialista antes de solicitar cambio. |

El máximo es un upgrade y un retry por tarea, compartidos entre todos los roles,
workers y sesiones. Los intentos iniciales normales de fases distintas no cuentan
como retry. Un upgrade que exige relanzar consume ambos saldos una sola vez;
cambiar de agente no los reinicia. Jarvis serializa las reservas en su registro
real de sesión; si lo pierde, bloquea hasta reconstruirlo con evidencia.

Cuando el host exige un worker nuevo, se conservan artefactos, versión y contadores
y se confirma el cierre del anterior antes de editar. El recibo distingue perfil
solicitado y efectivo, confirmación del host, evidencia, costos conocidos o null,
contadores, incertidumbres y próxima acción. Los detalles y esquemas de mensajes
están en la [política](../skills/escalacion-vengadores/references/policy.md).
