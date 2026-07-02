# Antes de diseñar, necesito hacerte unas preguntas

Revisé tu brief. Esto es lo que tengo claro y lo que me falta:

```
Stated requirements:
- SaaS dirigido a contadores freelance (o despachos pequeños)
- Funcionalidad central: gestión de facturas de sus clientes
- Entregable solicitado: dashboard principal

Open questions (lo que todavía necesito saber):
1. ¿Qué debe sentir el contador al abrir el dashboard — necesita actuar rápido sobre algo urgente, o revisar con calma el estado general?
2. ¿Hay herramientas o productos cuyo estilo le gusta o quiere evitar? (Linear, Notion, QuickBooks, Xero, un sistema bancario…)
3. ¿El uso principal es escritorio, o también necesita funcionar bien en tablet o móvil?
4. ¿Cuál es el primer número o dato que el contador busca cuando entra al dashboard?
5. ¿Qué NO debe sentir este producto? (banca corporativa genérica, startup con colores vivos, app de contabilidad antigua y densa)
```

---

## Mis respuestas asumidas (para proceder al diseño)

Como el brief es nuevo y no incluye referencia visual ni audiencia detallada, establezco las siguientes suposiciones antes de proceder:

**1. ¿Qué debe sentir el contador?**
Necesita actuar. El dashboard es su punto de entrada diario: lo primero que ve debe decirle qué está vencido, qué se cobra esta semana y qué clientes están bien. Es una herramienta de control y alarma temprana, no un informe bonito.

**2. ¿Referencias?**
No hay referencias explícitas. Asumo dirección cercana a Linear o Toggl: herramienta seria, datos primero, sin decoración. Lejos de QuickBooks (densa y arcaica) o de un dashboard de BI con gráficas de pastel dominantes.

**3. ¿Dispositivo?**
Escritorio como uso primario (el contador trabaja desde su oficina o laptop). Tablet como secundario. Se diseña con colapso responsivo incluido.

**4. ¿Primer dato al abrir?**
Lo que está vencido y sin cobrar. Eso determina el trabajo del día.

**5. ¿Qué NO debe ser?**
No banca corporativa verde. No startup colorida con gradientes. No app contable antigua con tablas comprimidas y sin jerarquía.

---

## Design read

```
Mode: Creation
Scope: Dashboard principal completo (shell de app + vista de resumen)
Client clarity level: Parcial — producto y audiencia claros, sin referencia visual
Desired outcome: Dashboard profesional y accionable para contador freelance
Visual direction: Herramienta seria, datos al frente, jerarquía por urgencia —
                 lo vencido y urgente visible antes que cualquier gráfica
Main UX/design risk: Caer en tarjetas de métricas genéricas que no reflejan
                     el flujo real del contador
Anti-generic decision: El elemento más prominente NO es una gráfica de ingresos.
                       Es la zona de "Facturas vencidas" — porque eso es lo que
                       el contador necesita resolver hoy.
```

---

## Dirección visual específica

Esta no es una paleta genérica "limpia y moderna". Estas decisiones emergen del producto:

- **Fondo cálido off-white (#F8F7F4):** No blanco clínico. El contador pasa horas en esta pantalla. Blanco puro cansa.
- **Sidebar oscuro (#1B2235):** Profesional, sin ser negro de moda. Diferencia claramente el navegador del contenido.
- **Sistema de estados con tres colores funcionales:**
  - Rojo (#DC2626): vencida — requiere acción hoy
  - Ámbar (#D97706): pendiente — próxima a vencer, en radar
  - Verde (#16A34A): pagada — cobrada, sin acción
- **Números con `font-variant-numeric: tabular-nums`:** Los valores monetarios se alinean en columna. No es cosmético, es legibilidad funcional.
- **Sin gradientes, sin glassmorphism, sin tarjetas con ícono decorativo gigante.**
- **Acento (#3B5BDB):** Azul funcional para acciones y links. No decorativo.

---

## Estructura del dashboard

**1. Barra de estadísticas (4 cifras):**
Por cobrar total · Vencido (destacado en rojo) · Cobrado este mes · Facturas activas

**2. Alerta de facturas vencidas:**
Strip visible cuando hay vencimientos. No lo oculto en una notificación — está en el flujo principal.

**3. Tabla de facturas vencidas:**
Cliente · Factura · Importe · Fecha de vencimiento · Días vencida · Acción directa ("Enviar recordatorio")

**4. Dos columnas:**
- Izquierda: próximas a vencer en los siguientes 30 días
- Derecha: pagos recibidos recientemente

**5. Estado de clientes principales:**
4 tarjetas compactas con monto pendiente y barra de estado visual

---

## Por qué este diseño es específico para este producto

- Un dashboard de analytics mostraría una gráfica de tendencia arriba. Este muestra facturas vencidas, porque un contador no necesita ver la tendencia de 6 meses cada mañana — necesita saber a quién llamar hoy.
- La acción "Enviar recordatorio" está directamente en la fila de la factura vencida, no en un menú de tres pasos.
- Los estados de color son un sistema, no decoración: rojo significa acción, ámbar significa prepararse, verde significa listo.
- La tipografía tabular hace que comparar $18,500 con $4,900 en una columna sea inmediato.

---

El dashboard completo está en `dashboard.html`.
