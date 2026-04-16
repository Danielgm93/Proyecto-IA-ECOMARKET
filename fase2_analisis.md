# Fase 2 — Evaluación de fortalezas, limitaciones y riesgos éticos

## 1. Introducción

La propuesta para EcoMarket consiste en una solución híbrida apoyada en IA generativa. Su valor principal es acelerar y mejorar la atención al cliente sin depender por completo de respuestas manuales. Sin embargo, una implementación de este tipo no debe evaluarse solo por su eficiencia, sino también por sus límites y sus implicaciones éticas.

## 2. Fortalezas

### 2.1 Reducción del tiempo de respuesta

La mayor fortaleza es la disminución del tiempo de atención para consultas repetitivas. Si el 80% de las solicitudes son sobre estado del pedido, devoluciones o características del producto, automatizar esas interacciones permitiría pasar de respuestas tardías a atención casi inmediata.

### 2.2 Disponibilidad 24/7

La solución puede responder en cualquier momento del día. Esto mejora la experiencia del cliente y reduce la dependencia de horarios rígidos de soporte.

### 2.3 Consistencia en la comunicación

Los agentes humanos pueden variar en tono, claridad o precisión. Un sistema bien diseñado puede mantener respuestas más uniformes, con lenguaje claro, estructura estable y mensajes alineados con la marca.

### 2.4 Escalabilidad operativa

A medida que EcoMarket crezca, el volumen de consultas también crecerá. La IA permite absorber parte de esa demanda sin aumentar el equipo humano al mismo ritmo.

### 2.5 Mejor uso del talento humano

Los agentes humanos pueden concentrarse en casos de mayor valor, como quejas complejas, recuperación de clientes inconformes o resolución de excepciones. Esto convierte a la IA en una herramienta de apoyo y no solo en un reemplazo operativo.

### 2.6 Posibilidad de mejora continua

El sistema puede mejorar con retroalimentación, registro de errores, nuevas reglas y refinamiento de prompts. Esto facilita una evolución progresiva.

## 3. Limitaciones

### 3.1 Dependencia de la calidad de los datos

Si la base de pedidos o las políticas contienen errores, el sistema responderá con errores. La IA no corrige mágicamente información defectuosa.

### 3.2 Dificultad en casos emocionalmente complejos

Aunque el modelo pueda sonar empático, no comprende el sufrimiento ni la frustración de la misma manera que un humano. En clientes molestos o en situaciones delicadas, una respuesta automática puede empeorar la experiencia.

### 3.3 Riesgo de ambigüedad en consultas mal formuladas

Si el cliente entrega información incompleta o confusa, el sistema puede responder con baja precisión o solicitar datos adicionales varias veces, generando fricción.

### 3.4 Mantenimiento constante

Las políticas de devolución, tiempos logísticos y catálogos cambian. Por eso la solución exige mantenimiento técnico y operativo permanente.

### 3.5 Dependencia tecnológica

Si el sistema tiene caídas, lentitud o fallos de integración, el servicio al cliente podría verse afectado de manera masiva.

## 4. Riesgos éticos

## 4.1 Alucinaciones

Uno de los principales riesgos es que el modelo genere información incorrecta con apariencia de certeza. Por ejemplo:

- inventar una fecha de entrega;
- afirmar que un producto puede devolverse cuando no aplica;
- prometer un reembolso no autorizado.

### Mitigación propuesta

- usar datos internos como única fuente autorizada para información operativa;
- prohibir que el modelo improvise cuando falte contexto;
- incluir respuestas de seguridad como: “No tengo información suficiente para confirmarlo”;
- escalar a humano cuando la consulta supere el nivel de confianza permitido.

## 4.2 Sesgo

El modelo podría producir diferencias injustas en el trato si reproduce patrones sesgados presentes en datos previos o en su comportamiento de lenguaje. Por ejemplo, podría responder de manera menos paciente, menos clara o menos útil a ciertos estilos de escritura, errores ortográficos o formas culturales de expresión.

### Mitigación propuesta

- revisar muestras de respuesta por segmentos de usuarios;
- definir lineamientos de trato uniforme;
- evaluar periódicamente tono, claridad y equidad;
- mantener supervisión humana sobre casos sensibles.

## 4.3 Privacidad y protección de datos

La atención al cliente usa información sensible: nombres, direcciones, teléfonos, historial de compra y datos de envío. Si estos datos se exponen innecesariamente al modelo o a sistemas terceros, se compromete la privacidad del cliente.

### Mitigación propuesta

- aplicar minimización de datos en el prompt;
- usar solo los campos necesarios para responder;
- ocultar datos completos cuando no sean indispensables;
- registrar accesos y auditorías;
- restringir la reutilización de conversaciones para entrenamiento sin controles adecuados.

## 4.4 Falta de transparencia

El cliente puede creer que está hablando con un humano cuando en realidad interactúa con un sistema automatizado. Esto puede afectar la confianza si no se comunica de forma honesta.

### Mitigación propuesta

- informar claramente cuando la atención inicial es asistida por IA;
- ofrecer siempre una ruta visible para contacto humano;
- explicar de manera simple los límites del asistente.

## 4.5 Impacto laboral

Existe el riesgo de que la automatización se use únicamente para reducir personal, en lugar de rediseñar el trabajo de manera responsable. Eso puede deteriorar el clima laboral y generar resistencia interna.

### Mitigación propuesta

- usar la IA para absorber tareas repetitivas y no como sustitución ciega del equipo;
- redefinir el rol del agente humano hacia resolución compleja, control de calidad y supervisión;
- capacitar al personal en uso y monitoreo del sistema.

## 4.6 Responsabilidad por errores

Si la IA da una instrucción equivocada que afecta un pedido o una devolución, surge una pregunta clave: ¿quién responde? La empresa no puede trasladar esa responsabilidad al sistema.

### Mitigación propuesta

- establecer trazabilidad de las respuestas;
- guardar contexto, decisión y versión del prompt usado;
- definir responsables humanos del proceso;
- limitar la autonomía de la IA en decisiones críticas.

## 5. Reflexión sobre el impacto empresarial real

Desde una perspectiva empresarial, la solución puede aportar valor importante si se implementa con criterio. El beneficio no está solo en bajar costos, sino en mejorar la experiencia del cliente y liberar tiempo del equipo humano. Sin embargo, si EcoMarket prioriza solo la automatización y descuida la supervisión, podría obtener el efecto contrario: respuestas más rápidas, pero menos confiables y menos humanas.

El verdadero éxito dependerá de mantener un equilibrio entre eficiencia, precisión, ética y experiencia del cliente.

## 6. Conclusión

La propuesta tiene fortalezas claras: rapidez, disponibilidad, consistencia y escalabilidad. No obstante, también presenta límites y riesgos reales, especialmente en alucinaciones, sesgos, privacidad, transparencia e impacto laboral. Por ello, la IA generativa no debe implementarse como reemplazo absoluto del soporte humano, sino como un sistema asistido, supervisado y gobernado por reglas claras. En el caso de EcoMarket, la mejor implementación sería aquella que automatiza lo repetitivo, protege al cliente y preserva la intervención humana donde realmente importa.
