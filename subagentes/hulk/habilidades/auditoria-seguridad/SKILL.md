---
name: auditoria-seguridad
description: Audita seguridad de código autorizado con Hulk, separando descubrimiento, verificación y reporte; exige evidencia y cobertura explícitas antes de declarar hallazgos.
---

# Auditoría de seguridad de Hulk

1. Confirmá tarea, SHA/snapshot, alcance autorizado, datos permitidos, modo y
   presupuesto TOTAL de llamadas. Reservá validación y reporte antes del hunting.
   Usá enfoque por defecto; completo exige pedido explícito. quick/standard/deep
   indican cobertura, no esfuerzo de razonamiento.
2. Aplicá la [adaptación](references/adaptacion.md) y la metodología fijada de
   [upstream](upstream/SKILL.md): [reconocimiento](upstream/RECONNAISSANCE.md),
   [búsqueda](upstream/HUNTING.md) y
   [validación/reporte](upstream/VALIDATION-AND-REPORTING.md).
   Sus instrucciones de coordinación no se trasladan al worker.
3. Jarvis es el único coordinador: invoca workers Hulk descubridor, verificador
   y reportero separados. Ant-Man prepara recon/contexto reutilizable. Hulk no
   redelega ni escribe fixes; Thor corrige, Guardianes producen regresiones y
   Pantera propone reglas. Jarvis no redacta informes técnicos ni ejecuta tests.
4. Antes de ejecutar código, exigí sandbox de SO conforme a upstream y permisos
   autorizados. Sin soporte, solo lectura: candidatos no evaluados quedan pendientes en el
   ledger; solo un verificador puede decidir needs_validation con bloqueo preciso. No habilites red, dependencias ni modelos
   automáticamente. Respetá límites de datos/proveedor.
5. Designá un único escritor técnico del informe, con salida separada del código
   y permisos explícitos. Conservá versión, coverage y fingerprint. Los validadores
   Node comprueban estructura, no veracidad. No reduzcas evidencia para satisfacer
   presupuestos o límites de escalada: informá pendientes y cobertura incompleta.
6. Entregá fuentes, evidencia, límites y próxima acción. Conservá pin y licencia;
   no afirmes ejecución funcional por disponer de esta skill.
