# gssr-toolbelt

Colección de Agent Skills reutilizables para asistentes de código, alineadas con el estándar
[agentskills.io](https://agentskills.io/specification): frontmatter YAML, divulgación
progresiva (`SKILL.md` + `references/` + `scripts/`) y evaluaciones por skill.

## Estructura

```text
.github/
  copilot-instructions.md
.claude-plugin/
  plugin.json
  marketplace.json
skills/
  llms.txt
  <skill-name>/
    SKILL.md
    references/      # material que se carga solo cuando hace falta
    scripts/         # comprobaciones deterministas
    evals/evals.json # prompts y aserciones de prueba
scripts/
  validate-skills.py
evals/
  fixtures/          # app heredada con defectos deliberados
  runs/              # salidas de pruebas (ignorado por git)
  build-evals.py
  setup_runs.py
skill.sh
```

## Cómo usar

1. Copia la carpeta del skill que necesites a tu directorio de skills (`.claude/skills/`,
   `.agents/skills/` o el que use tu cliente).
2. O usa el repo como plugin/colección: el índice está en `skills/llms.txt`.
3. Para crear un skill nuevo, duplica `skills/skill-template/` y sigue la guía.

## Validar

```bash
./skill.sh validate
# o
python3 scripts/validate-skills.py
```

Comprueba frontmatter, nombre contra carpeta, longitud de descripción, tamaño del cuerpo,
referencias inexistentes y presencia de evaluaciones.

## Probar

```bash
python3 evals/build-evals.py      # genera skills/*/evals/evals.json
python3 evals/setup_runs.py       # copia el fixture a evals/runs/<skill>/repo
```

Después ejecuta cada prompt de `evals/evals.json` con un agente que cargue el `SKILL.md`
correspondiente, guarda el informe en `evals/runs/<skill>/outputs/` y contrasta las
aserciones. Ver `evals/README.md`.

## Convenciones

- Cada skill vive en su propia carpeta en `skills/`.
- `name` en kebab-case y debe coincidir con la carpeta.
- La descripción debe decir **qué hace** y **cuándo usarlo** (es el mecanismo de activación).
- `SKILL.md` idealmente < 500 líneas; el detalle va en `references/`.
- Los scripts no deben requerir dependencias de terceros cuando sea posible.
- Las evaluaciones deben nombrar el fallo que previenen, no solo "funciona".

## Skills incluidos

Producto: `feature-interrogation`, `acceptance-criteria`, `simplest-solution`.

Ingeniería: `code-review`, `debug-root-cause`, `refactor-safely`, `test-strategy`,
`security-review`, `performance-engineering`.

Datos/APIs: `migration-safety`, `api-contract`.

Craft/diseño: `anti-ai-slop`, `clear-writing`, `pr-craft`, `accessibility-audit`,
`design-system-discipline`, `motion-quality`, `image-to-ui`, `tasteful-ui-ux`,
`frontend-polish`.

Entrega/operaciones: `observability-first`, `release-readiness`, `dependency-hygiene`.

Meta: `skill-template`.

## Licencia

MIT.
