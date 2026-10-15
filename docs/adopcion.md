# Adopción en un proyecto destino

1. Seleccionar una versión de Vengadores mediante tag o SHA.
2. Copiar la plantilla de configuración a `.vengadores/config.yaml` y completar rutas
   y comandos reales. Es un contrato propuesto; no existe todavía un lector automático.
3. Indicar en las instrucciones del destino dónde consultar Vengadores y su versión.
4. Referenciar el skill de delegación existente. Jarvis debe leer su contrato antes
   de delegar; si falta, detener la delegación y registrar la dependencia pendiente.
5. Identificar `AGENTS.md` y las memorias existentes. No reemplazarlas con las plantillas.
6. Guardar especificaciones, planes e informes en `.vengadores/tasks/<id>/` o la ruta
   que establezca el destino. Vincular artefactos externos cuando sean voluminosos.
7. Definir controles de merge, actualización de grafo, despliegue y recuperación.
8. Ejecutar una tarea pequeña siguiendo el flujo y evaluar memoria, costo y errores.

Se puede consumir Vengadores mediante un checkout separado o un submódulo fijado
a commit. Cambiar su versión debe ser explícito y revisable; no seguir automáticamente
la rama principal para tareas ya iniciadas. El proveedor cloud y la plataforma del
grafo son configurables y todavía no están seleccionados.

Una organización reutiliza reglas globales sin mezclar contextos privados: cada
proyecto tiene identidad, configuración, permisos, artefactos y memoria propios.

