# Mi experiencia

## Proyecto 1: Optimización de plataforma web en una empresa de logística

- **Problema y contexto:** La plataforma tenía fallas de funcionamiento y lógica en sus módulos: condiciones de carrera (*race conditions*), dificultad para soportar el volumen de llamadas a la API con muchos usuarios en línea y componentes poco optimizados.
- **Tecnologías:** Angular en el frontend y .NET en el backend, que eran la base de la plataforma.
- **Mi contribución:** Desarrollé gran parte de los componentes del frontend, corregí su lógica, optimicé sus llamadas a la API, implementé patrones de diseño y solucioné condiciones de carrera.
- **Decisión difícil:** Una tabla superaba el millón de registros y traerla era demasiado pesado para la web. Implementé una carga por partes mediante un worker en paralelo, activado al entrar al módulo. Limité la caché en memoria a 8.000 registros para responder de inmediato al volver, y pasado un minuto desde la primera carga se actualizaba con lo último de la base de datos. Esto mejoró el tiempo de respuesta.
- **Qué cambiaría hoy:** Evitaría la sobreingeniería en módulos básicos. Quise cubrir posibles problemas futuros y agregué lógica que esos componentes no necesitaban; hoy ajustaría la complejidad a la necesidad real.

## Proyecto 2: App de delivery para el Chocó (en desarrollo)

- **Problema y contexto:** El Chocó tiene mucha precariedad en tecnología y aplicaciones de este tipo; queremos ser pioneros llevando una plataforma de domicilios que conecte clientes, negocios y domiciliarios.
- **Tecnologías:** React y Vite en la web, empaquetada con Capacitor para iOS y Android reutilizando el código; Node.js y Express en la API; PostgreSQL con Sequelize para los datos; Socket.IO para comunicación en tiempo real y Wompi para pagos.
- **Mi contribución:** Trabajo en equipo como mano derecha del arquitecto de software. Implementé funciones de frontend y backend: registro por roles, prevención de pedidos duplicados (bloqueo de doble envío y clave de idempotencia), cálculo del pago al domiciliario, cancelaciones con penalización, asignación de domiciliarios, notificaciones y quejas, además de integrar ramas. Usamos IA para generar código, dejando soporte.
- **Decisión difícil:** Integrar una pasarela de pagos bien fundamentada, para lo cual el equipo eligió Wompi, y calcular el precio del domicilio. El proyecto lo resuelve con tarifa por distancia más recargos por lluvia y horario nocturno, usando la misma cuenta al cotizar y al crear el pedido.
- **Qué cambiaría hoy:** Por ahora mantendría el rumbo. Ha sido un proceso de mucho aprendizaje, en especial sobre comunicación en tiempo real con WebSockets.

