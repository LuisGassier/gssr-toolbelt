# Evaluaciones

Cada skill incluye `evals/evals.json` con uno o más casos. Hay dos fixtures:

- `fixtures/legacy-app`: una app Express/React con defectos deliberados de seguridad,
  rendimiento, accesibilidad, migraciones, API, copy y testing.
- `fixtures/ui-reference`: un screenshot de 1440×900 para el skill `image-to-ui`. La fuente
  está en `fixtures/ui-reference-src/` y no se copia a la ejecución.

El resultado consolidado está en `RESULTS.md`.

## Ciclo de prueba

1. Generar las evaluaciones:

   ```bash
   python3 evals/build-evals.py
   ```

2. Preparar una copia aislada por skill:

   ```bash
   python3 evals/setup_runs.py
   ```

   Resultado:

   ```text
   evals/runs/<skill>/repo/      copia editable del fixture
   evals/runs/<skill>/outputs/   informe y artefactos
   ```

3. Ejecutar el prompt de `evals.json` con un agente que cargue el `SKILL.md` de esa carpeta.
   El agente debe trabajar solo en su `repo/` y escribir `outputs/report.md`.

4. Contrastar cada aserción contra el informe y los archivos modificados. Una aserción pasa
   solo si hay evidencia verificable (cita, archivo, línea o cambio).

5. Registrar el resultado en `evals/RESULTS.md` con: skill, veredicto, aserciones
   fallidas, causa y mejora aplicada.

## Medir y comparar imágenes

El skill `image-to-ui` incluye `scripts/image_probe.py` (requiere Pillow):

```bash
python3 skills/image-to-ui/scripts/image_probe.py info reference.png --dpr 1
python3 skills/image-to-ui/scripts/image_probe.py palette reference.png --colors 16
python3 skills/image-to-ui/scripts/image_probe.py sample reference.png --points "24,24;232,64" --radius 2
python3 skills/image-to-ui/scripts/image_probe.py grid reference.png --step 100 --labels --out grid.png
python3 skills/image-to-ui/scripts/image_probe.py diff reference.png render.png \
  --tolerance 8 --out diff.png --overlay overlay.png --fail-over 0.5
```

## Reglas

- No ejecutar `npm install` ni acceder a red durante las pruebas del fixture.
- No compartir la misma copia entre skills; cada ejecución debe ser independiente.
- Las aserciones deben nombrar el fallo que previenen, no una preferencia de estilo.
- Un skill que no dispara con su prompt positivo, o que dispara con un near-miss, necesita
  ajustar la `description`, no el cuerpo.
- Las pruebas son una muestra; no sustituyen la revisión humana.

## Prueba de disparo (trigger)

`trigger-queries.json` contiene prompts positivos y near-misses. Para probarlos, presenta a
un agente solo el catálogo `name + description` y pídele que elija el skill (o ninguno) para
cada prompt. Un positivo debe elegir el skill correcto; un near-miss no debe elegirlo.
Ajusta la descripción si hay confusión sistemática.
