# Método de creación

## Contrato previo

Registrar objetivo, disparadores positivos, exclusiones, host, herramientas reales,
permisos, entradas, salida, versión de fuentes y aceptación. Si falta una decisión
que cambia el contrato, pedirla; las preferencias rutinarias pueden resolverse con
las convenciones del destino. Buscar skills existentes y extender o reutilizar
antes de duplicar. Jarvis delega la autoría; Nick Fury escribe los artefactos.

## Crear una skill

- Carpeta y `name`: mismo identificador, minúsculas/números/guiones, 1–64 caracteres,
  sin guiones consecutivos ni extremos. Usar `SKILL.md` con YAML y cuerpo Markdown.
- `description`: qué hace y cuándo activarla. Evitar listas de sinónimos y contenido
  que pertenece al procedimiento. Agregar campos opcionales solo si son necesarios.
- Cuerpo: decisiones mínimas, herramientas/dependencias, pasos y resultado. Los
  límites que siempre aplican permanecen aquí, no ocultos en una referencia opcional.
- Referencias: temas independientes, enlaces directos desde el núcleo con condición
  de carga. No obligar a leer todos los archivos en cada activación. Una fuente
  canónica por regla; los wrappers enlazan a ella.
- Scripts: operaciones repetibles; exponer parámetros y errores útiles. Ejecutarlos
  cuando haga falta, en vez de cargar todo su código o logs como contexto.

## Crear un subagente

Un rol escrito no crea un proceso. Definir responsabilidad única, contrato de
entrada/salida, capacidad requerida y propietario de integración.

OpenCode admite perfiles Markdown en `.opencode/agents/`. El nombre del archivo
identifica el agente; `mode: subagent` lo distingue del coordinador. Configurar solo
los permisos que necesita dentro de la autorización del proyecto. No fijar modelos
o herramientas inexistentes. Una skill se carga dentro de ese agente cuando aplica.

En el adaptador Codex `collaboration`, el rol se entrega en el prompt de una llamada
real. No inventar un formato universal de archivo de agente para todos los hosts.
Usar la skill de delegación vinculada y confirmar el esquema expuesto por el host.

El prompt recibe objetivo, revisión, alcance, referencias, entregable y límites.
Cada ejecutor que escribe usa worktree propio; no heredar todo el historial ni
duplicar las instrucciones de Jarvis. Los workers no redelegan salvo autorización
explícita. Nick Fury pide a Jarvis el ensayo de ejecución; no se convierte en otro
coordinador de la fábrica.

## Comprobación y entrega

1. Auditar los campos requeridos y enlaces con `scripts/audit.py`; para YAML avanzado
   usar además un validador completo compatible con Agent Skills. El auditor local
   no certifica todos los campos opcionales del estándar.
2. Verificar activación pertinente, una solicitud fuera de alcance y una dependencia
   ausente. Evaluar comportamiento, no solo que el archivo exista.
3. Para un agente, confirmar ID real, respuesta, herramientas y límites del host.
   Probar los modelos/hosts realmente utilizados; no extrapolar entre proveedores.
4. Comparar contexto y calidad antes/después si el cambio se presenta como una
   optimización. Conservar revisión y método, distinguir tokens, bytes y latencia.
5. Informar archivos generados, comprobaciones y bloqueos. No registrar como ahorro
   una reducción de tamaño sin medir tokens del recorrido correspondiente.
