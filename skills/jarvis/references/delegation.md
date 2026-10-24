# Vinculación de la skill de delegación

El configurador del repositorio instala Jarvis y crea `.vengadores/jarvis.json`.
`delegation_skill` apunta por defecto a la skill incluida `delegacion-vengadores`,
instalada como hermana de Jarvis. Con `--delegation-skill` puede vincularse otra
skill externa. La interfaz se lee de la dependencia y se verifica frente al host.

Ejemplo de configuración creada por el instalador:

```json
{
  "schema_version": 1,
  "host": "opencode",
  "skill_directory": ".opencode/skills/jarvis",
  "delegation_skill": "/ruta/proyecto/.opencode/skills/delegacion-vengadores/SKILL.md"
}
```

Con la carpeta de Vengadores agregada al PATH de la terminal, instalar y vincular
desde el proyecto destino:

```bash
vengadores unidos
```

Para Codex, usar `vengadores unidos --host codex`; la ubicación es `.agents/skills/jarvis`.
Reabrir la sesión del host para que descubra la nueva skill. También puede abrirse
su `SKILL.md` explícitamente si el host permite cargar skills por ruta.

Si Jarvis ya está instalado, vincular la dependencia:

```bash
python3 scripts/configure_jarvis.py bind --project /ruta/proyecto --delegation-skill /ruta/real/delegacion/SKILL.md
python3 scripts/configure_jarvis.py check --project /ruta/proyecto
```

Si la dependencia se elimina o no existe, el estado es `bloqueado`. Vincular un archivo válido
comprueba su presencia y formato; la compatibilidad de sus herramientas se comprueba
en el host al activar Jarvis. No se ejecutan scripts arbitrarios de la dependencia.

La configuración de vínculo es local y no debe llevar rutas privadas al repositorio.
Los comandos, permisos, presupuestos y datos del proyecto pertenecen a su configuración
general. El vínculo no amplía permisos ni instala herramientas de ejecución.
