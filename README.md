# gssr-toolbelt

Repositorio base de skills reutilizables para asistentes de codigo.

## Estructura

```text
.github/
  copilot-instructions.md
.claude-plugin/
  plugin.json
  marketplace.json
skills/
  llms.txt
  skill-template/
    SKILL.md
  frontend-polish/
    SKILL.md
skill.sh
LICENSE
README.md
```

## Como usar

1. Duplica `skills/skill-template/` para crear un skill nuevo.
2. Renombra la carpeta con un nombre claro en kebab-case.
3. Edita su `SKILL.md` con alcance, reglas y pasos.
4. Versiona los cambios con Git.

## Convenciones

- Cada skill vive en su propia carpeta.
- Cada skill define su contenido en `SKILL.md`.
- Evita instrucciones ambiguas: usa pasos accionables.
- Mantiene compatibilidad con Copilot Chat y agentes similares.

## Proximos pasos sugeridos

- Agregar `CHANGELOG.md` cuando empieces a publicar versiones.
- Agregar tests de prompts o ejemplos de entrada/salida por skill.
- Automatizar validaciones con scripts si el repositorio crece.
