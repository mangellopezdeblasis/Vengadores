---
name: entrega
description: Integración y entrega verificada de Soldado del Invierno. Al integrar en dev y desplegar una candidata con controles requeridos aprobados.
---

# Integración y entrega verificada

Confirmá candidata, base dev vigente, evidencia de controles y autorización de integración/despliegue. Aplicá las políticas y herramientas reales del destino; verificá que los controles correspondan al SHA final.

Integrá en la rama actual registrada por Jarvis al iniciar el flujo (dev solo si el destino lo exige) y desplegá según la tarea. Al terminar, con la candidata integrada, eliminá los worktrees y ramas temporales del flujo que ya no tengan trabajo sin integrar, y dejá el checkout en esa rama actual; no borres worktrees con cambios sin integrar, informalos como pendientes. Confirmá el SHA integrado y resultado del despliegue para Jarvis. Guardianes de la Galaxia ejecutan los E2E con datos aislados y registran resultado, evidencia y necesidad de refrescar el grafo para Jarvis. Ante fallo, seguí la política autorizada de recuperación considerando compatibilidad de código y datos; si falta, informá el bloqueo. No declares despliegue exitoso mientras siga pendiente.
