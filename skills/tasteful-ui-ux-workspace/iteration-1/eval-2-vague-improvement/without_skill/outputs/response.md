# Rediseño de la página de login

## Lo que está mal con la versión actual

La página original tiene exactamente los patrones que hacen que algo se vea generado por IA:

1. **Fondo con gradiente púrpura diagonal** (`#667eea → #764ba2`) — es el gradiente más clonado de los últimos 5 años. Aparece en miles de templates de Tailwind y en prácticamente toda UI generada automáticamente.
2. **Tarjeta blanca flotando sobre el gradiente** — la combinación gradiente + card es el layout más genérico que existe. No tiene intención de diseño, es el default de todo template.
3. **Color primario indigo #4F46E5** — es literalmente el color `indigo-600` de Tailwind. Lo usa la mitad del internet.
4. **Copy sin personalidad**: "Welcome back! Please sign in to continue." — no dice nada sobre el producto ni crea ninguna conexión.
5. **Sombra decorativa exagerada** (`box-shadow: 0 20px 60px`) — añade dramatismo innecesario sin aportar jerarquía visual real.
6. **Glassmorphism ausente aquí pero el patrón card-flotante es su primo directo** — mismo impulso: "agrega profundidad visual con efectos", mismo resultado genérico.

## Dirección de diseño

En lugar del enfoque "tarjeta sobre fondo decorativo", voy hacia un **layout editorial de dos columnas**:

- **Panel izquierdo oscuro** (sin gradiente, color sólido y deliberado): espacio de marca con nombre del producto, una propuesta de valor concisa y dos o tres puntos de apoyo. El negro/charcoal casi-negro da seriedad y contraste.
- **Panel derecho blanco**: el formulario limpio, con espacio generoso y tipografía clara. Sin decoración competitiva.
- **Color de acento**: terracota cálida (`#d4622a`) en lugar de indigo. Menos utilizada, más carácter, crea una identidad visual real.
- **Tipografía**: Inter — limpia y legible, con jerarquía establecida por peso y tamaño, no por efectos.
- **Sin gradientes, sin sombras decorativas, sin glassmorphism.**

El resultado se ve como una decisión de diseño, no como el output de un prompt.
