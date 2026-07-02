# Dashboard para ContaFlow — SaaS para Contadores Freelance

## Dirección de diseño

He diseñado un dashboard orientado a **contadores freelance que manejan múltiples clientes** simultáneamente. Las prioridades de diseño son:

1. **Claridad financiera inmediata** — el contador necesita saber en segundos cuánto facturó, cuánto le deben y qué está vencido.
2. **Alertas de acción** — las facturas vencidas son un problema crítico para el flujo de caja; se priorizan visualmente.
3. **Visual profesional y de confianza** — el esquema índigo/pizarra transmite solidez contable sin ser frío ni corporativo.
4. **Densidad informacional controlada** — mucha información visible sin sentirse abrumador, gracias a la jerarquía tipográfica y el uso de espacio.

---

## Lo que incluye el dashboard

### Sidebar de navegación (izquierda)
- Logo **ContaFlow** con marca visual distintiva
- Secciones: **Dashboard**, **Facturas** (con badge de 3 pendientes de atención), **Clientes**, **Pagos**, **Reportes**, **Configuración** y **Cerrar sesión**
- Perfil de usuario en la parte inferior con nombre y rol
- Indicador visual de ítem activo con barra lateral de color

### Barra superior
- Título de página con fecha actual
- Buscador global (facturas, clientes)
- Botón de notificaciones con punto rojo
- Acceso rápido al calendario
- Chip de perfil del usuario

### Banner de alerta contextual
- Aviso inmediato sobre las 3 facturas vencidas ($7,130 MXN), con CTA directo para verlas
- Descartable para no interrumpir el flujo si ya se leyó

### Saludo personalizado + acciones rápidas
- Saludo con nombre del contador
- Dos botones principales: **Exportar** y **+ Nueva Factura**

### 4 tarjetas KPI (métricas clave)
| Métrica | Valor | Contexto |
|---|---|---|
| Facturado este mes | $47,250 MXN | +12.3% vs mes anterior |
| Por cobrar | $28,350 MXN | 8 facturas pendientes |
| Vencido | $7,130 MXN | 3 facturas — requiere atención |
| Clientes activos | 12 | +2 nuevos este mes |

Cada tarjeta tiene su color de estado (índigo / amarillo / rojo / verde) y un badge con el cambio relativo.

### Gráfica de ingresos (línea + área, últimos 6 meses)
- Curva suavizada con relleno de gradiente
- Punto activo resaltado (mes actual) con tooltip de valor
- Selector de período: 6M / 12M / 2A
- Ejes con etiquetas legibles

### Donut de estado de facturas
- 47 facturas totales: 28 pagadas (60%), 14 pendientes (30%), 5 vencidas (10%)
- Agujero central con total
- Leyenda con conteos y porcentajes
- Barra de progreso hacia la meta mensual de cobro (75%)

### Tabla de facturas recientes
- Columnas: N.° de factura, Cliente (con avatar de color), Estado, Fecha, Monto, Acción
- Estados con badges de color (verde / amarillo / rojo)
- Hover state en filas
- Tabs de filtro: Todas / Pendientes / Vencidas
- Footer con paginación ligera ("Ver todas")

### Panel derecho — Próximos vencimientos
- Tres facturas ordenadas por urgencia
- Código de color: rojo (3 días), amarillo (8 días), índigo (15 días)
- Nombre del cliente, número de factura y monto

### Panel derecho — Top clientes
- Los 3 clientes con mayor ingreso total
- Barra de progreso relativa al cliente con mayor facturación
- Número de facturas y monto acumulado

---

## Decisiones de UX relevantes

- **El estado "Vencido" aparece en tres lugares**: tarjeta KPI, banner de alerta y tabla — porque es la acción más urgente para un contador freelance.
- **La sidebar usa un fondo oscuro** (indigo-950) para crear contraste con el área de trabajo, ayudando a la orientación espacial.
- **Los avatares de color** para cada cliente dan identidad visual rápida en la tabla, evitando leer el nombre completo cada vez.
- **Las tarjetas KPI tienen una franja de color superior**, no todo el card coloreado — mantiene limpieza visual y suficiente señal de estado.
- **El donut incluye una meta de cobro mensual** (75%) porque un contador freelance necesita saber si va bien, no solo cuántas facturas tiene.
- **Fuente Inter** — estándar de la industria SaaS; excelente legibilidad en cifras y texto denso.

---

## Entregable

El archivo `dashboard.html` es completamente autónomo: todos los estilos están en `<style>`, usa solo SVG inline para íconos y gráficas (sin dependencias de JS ni librerías externas), y carga Inter desde Google Fonts como única dependencia de red.
