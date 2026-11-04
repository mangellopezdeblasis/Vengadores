# Revisión de cambios y evidencia

Aplicá estas comprobaciones solo a los flujos y superficies afectados; las reglas y contratos del destino prevalecen. Documentá alcance, revisión y árbol con cambios, fuentes y límites. Un checklist no demuestra cobertura ni aprueba una integración.

## Integración y artefactos

- Compará el candidato con su base y, ante un merge, con ambos padres: marcadores de conflicto, archivos o métodos perdidos, cambios ajenos revertidos y consumidores huérfanos. Considerá código, configuración, documentación y recursos versionados. No recomiendes reescribir historial sin evaluar su publicación y autorización.
- Contrastá archivos requeridos, hash, generación y copia en los Dockerfiles y pipelines realmente usados. En workers y modelos verificá rutas, base path, tipos de contenido, CSP, navegador y recursos del paquete desplegado. Un recurso HTTP 200 o una prueba con worker simulado no demuestra inicialización ni ejecución real. Mantené alternativas manuales existentes.
- Comprobá lint, tipos y construcción cuando corresponda; distinguí fallas introducidas de previas. No presumas que una ejecución vieja aplica al SHA o diff actual. Identificá dependencias, declaraciones sin consumidores y duplicaciones solo tras revisar sus usos y estados asociados.

## Escritura y recuperación

- Seguí UI, servicio, API y persistencia para alta, edición, adjuntos y eliminación: datos, ID retornado, estado del formulario, permisos según creación/actualización y recarga. Verificá que el guardado parcial no pierda estado ni permita reenviar erróneamente; que cada bloqueo de navegación explique cómo continuar y que errores repetidos sigan visibles.
- Para timeout, desconexión o respuesta 5xx tras una escritura, considerá que el servidor puede haber confirmado o seguir procesando. Un GET sin coincidencias, un mock o un cambio en la UI no prueba el rechazo ni autoriza un reenvío ciego. Verificá identidad estable de operación, vinculación a actor/recurso/contenido, persistencia atómica, reintentos simultáneos, recuperación tras recarga y rotación de claves. Si faltan garantías, informá el estado incierto y la salida segura pendiente.
- Contrastá validación y obligatoriedad entre UI, API, persistencia y reglas efectivas. Diferenciá ID inválido del cuerpo y recurso del path, catálogos mostrados y valores aceptados, semántica de NULL y permisos efectivos. No infieras la regla de negocio solo de un dato o de una implementación alternativa.
- Para componentes compartidos y manejo de errores, inspeccioná consumidores con reglas diferentes; distinguí un resultado opcional no encontrado de una falla de servicio y comprobá que un cambio de aviso o limpieza no altere otros formularios. Tratá tiempo, fechas, zona, formato y compatibilidad conforme al contrato real y sus consumidores; no afirmes desplazamientos sin trazar la conversión.

## Límites, rendimiento y entrega

- Verificá ownership de datos, escritores concurrentes, transacciones, restricciones, migraciones y permisos efectivos antes de atribuir seguridad a una anotación o mock. Marcar como pendiente lo no verificado en base real o en el ambiente. La documentación de una excepción no elimina una carrera.
- Revisá N+1, consultas completas dentro de ciclos y transferencia repetida de binarios/base64. Al proponer batching, preservá identidad y garantías ante éxitos parciales y concurrencia; distinguí un costo observado de una medición de rendimiento pendiente.
- Separá hechos comprobados, hipótesis, riesgos y sugerencias; para cada hallazgo indicá disparador, recorrido, impacto, evidencia y severidad justificada. Identificá pruebas ejecutadas y sus límites, roles efectivos, esquema, despliegue y runtime como verificados o pendientes; nunca presentes mocks ni checks estructurales como prueba de integración. Sanitizá identificadores, contenido privado y secretos. Ante una corrección, verificá consumidores y casos adversos sobre la revisión nueva antes de cambiar su estado.
