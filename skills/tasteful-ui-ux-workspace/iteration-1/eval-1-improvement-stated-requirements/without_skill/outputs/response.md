# Rediseño Editorial Oscuro de FlowSync

## Dirección de diseño

Tres cambios principales guiaron la revisión:

**1. Paleta oscura editorial**
Cambié toda la página a un sistema de color oscuro usando casi-negro (`#0A0A0C`) como fondo base, con variantes ligeramente más claras para alternar secciones (`#0E0E12`). Los textos usan una escala de blancos cálidos — el cuerpo principal en `#F0EDE8` (blanco marfil ligeramente cálido, más editorial que puro blanco), los textos secundarios en `#9E9BAA`, y los terciarios en `#5E5B6C`. El acento cambió de `#4F46E5` puro a `#7C6FEA` — más suave contra negro, evita la vibración visual.

**2. Tipografía editorial**
Introduje *Playfair Display* (serif, peso 700/800) para todos los títulos principales y el número de precios. La combinación serif en dark background da el tono editorial característico de publicaciones como The Economist o revistas de diseño tech. Los subtítulos y cuerpo siguen en Inter para contraste de registro. Los títulos usan `letter-spacing: -0.025em` para el ajuste óptico típico de tipo editorial en cuerpos grandes.

**3. Pricing resaltado**
El pricing section recibió el tratamiento más diferenciado:
- Números de precio en Playfair Display a 56px — imposibles de ignorar
- Tarjeta "Popular" con doble borde (outline + box-shadow de color), gradient de fondo sutil, y badge flotante "Most Popular"
- Los botones CTA de las tarjetas tienen personalidades distintas: los planes lateral son ghost buttons (borde sutil), el plan Popular tiene el botón sólido con glow
- Descripción de una línea por plan que contextualiza a quién va dirigido
- Checkmarks SVG custom en lugar del `✓` de texto — más refinado

## Qué no toqué

- **Navegación**: HTML y CSS exactamente igual al original. Color blanco de fondo, logo indigo, links grises, CTA button igual.
- **Email form**: HTML y CSS idénticos — input con border gris, botón `#4F46E5`, mismas dimensiones y border-radius.

## Cambios adicionales de calidad

- Bloom radial sutil detrás del hero (radial gradient en posición absoluta) que da profundidad sin ser kitsch
- `eyebrow label` en hero con dot animado que contextualiza "Introducing FlowSync 2.0"
- Separadores entre secciones como líneas degradadas de center-out (no líneas duras)
- Las feature cards se organizan como grid unificado con separadores de 1px — más editorial que cards sueltas
- Hover states en todas las tarjetas (sutil transform Y)
- `-webkit-font-smoothing: antialiased` en body para rendering de fuentes más limpio en macOS sobre fondos oscuros
