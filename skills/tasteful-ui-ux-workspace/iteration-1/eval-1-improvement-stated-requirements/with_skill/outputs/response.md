# Respuesta al cliente

## Requisitos declarados

Antes de proceder, listando exactamente lo que pediste:

- La landing page debe sentirse **más editorial y oscura**
- **No tocar la navegación** de arriba
- **No tocar el formulario de email**
- El **pricing debe resaltar más**

No quedan preguntas abiertas — estos requisitos dan suficiente dirección para proceder.

---

## Design read

**Mode:** Improvement
**Scope:** Landing page completa — hero, features, pricing, testimonials, footer. Nav y email form excluidos del rediseño.
**Nivel de claridad del cliente:** Dirección clara con restricciones explícitas.

**Estado actual:** Plantilla SaaS de fondo blanco con acento índigo. Genérica — hero centrado, tres tarjetas de características idénticas en tamaño y peso, sección de pricing que visualmente no se diferencia del resto. Sensación de template AI, no de producto con carácter propio.

**Outcome deseado:** Atmósfera oscura y editorial. Pricing como el momento de conversión visual más fuerte de la página.

**Traducción de "editorial y oscura" para FlowSync:**
- No el dark SaaS genérico con purple glow. Más parecido a una publicación técnica seria o una herramienta de alto nivel.
- Fondo casi negro (#0C0C0E), texto en blanco cálido (#F0ECE6), acento índigo preservado.
- Tipografía serif para los titulares (Georgia) — crea autoridad editorial. Sans-serif para el body — legibilidad técnica.
- Espacio generoso. Sin decoración innecesaria.
- La sección de pricing recibe tratamiento visual propio: tarjeta popular con fondo de acento sólido (índigo con texto blanco), números de precio en serif y más grandes, sección diferenciada visualmente del resto de la página.

**Riesgo principal:** Cambiar plantilla clara por plantilla oscura sin diferencia conceptual. Evitado al cambiar el sistema tipográfico (serif + sans), el ritmo de secciones, y el tratamiento de la jerarquía de pricing.

**Preservar:** HTML y CSS del nav exactamente. HTML y CSS del email form exactamente. Todo el contenido. Acento índigo (#4F46E5 / #6366F1).
**Cambiar:** Sistema de color (fondo oscuro), escala tipográfica (serif para titulares), peso visual de pricing, ritmo de secciones, tratamiento de tarjetas de características.

**Nivel de intervención:** Net-new design direction aplicada a la capa visual y tipográfica. La estructura HTML es compatible — el rediseño es de piel, no de huesos.

---

## Lo que entregué

**Hero:** Fondo oscuro base. H1 en Georgia serif con la palabra "Workflow" en itálica para el tratamiento editorial. Subtítulo en gris apagado. Botón primario (índigo) + botón secundario (borde claro, texto claro — funciona sobre oscuro). Email form preservado exactamente.

**Features:** Sección con fondo ligeramente más claro (#111115). Las tres tarjetas están unidas en un panel horizontal con divisores de línea fina en lugar de tarjetas flotantes separadas — más editorial, menos template. Títulos de tarjetas en serif.

**Pricing:** Sección con fondo propio (#0E0E13) y bordes horizontales para aislarla del resto. Título más grande (48px vs 40px en el resto). Subtítulo agregado. Tarjeta Pro con fondo índigo sólido y texto blanco — contraste máximo, no sólo un borde de color. Números de precio en serif a 56px. Lista de beneficios con checkmarks SVG circulares. Dividers entre precio y lista para separar la información.

**Testimonials:** Cita decorativa en serif grande como elemento editorial. Tarjetas sobre fondo oscuro con borde sutil.

**Footer:** Mínimo.

**Responsive:** Columnas colapsan a una en mobile. Hero buttons y email form en columna. Padding reducido en mobile. Tipografía ajustada.

---

La navegación y el formulario de email no fueron tocados — su HTML y CSS son exactamente los del original. Agregué `background: #fff` al nav para que su apariencia visual se preserve en el contexto del nuevo fondo oscuro.
