# Fase 1 — Selección y justificación del modelo de IA

## 1. Problema a resolver

EcoMarket es una empresa de comercio electrónico que enfrenta un cuello de botella en su área de atención al cliente. La empresa recibe miles de consultas diarias a través de chat, correo electrónico y redes sociales. Aproximadamente el 80% de esas consultas son repetitivas, principalmente sobre estado del pedido, devoluciones y características del producto. El 20% restante corresponde a casos más complejos, por ejemplo quejas, problemas técnicos o sugerencias, que requieren mayor juicio, empatía y eventualmente intervención humana.

El problema central no es únicamente “responder más rápido”, sino **responder con precisión, consistencia y buen tono**, reduciendo el tiempo de atención sin deteriorar la experiencia del cliente.

## 2. Modelo propuesto

Propongo una **solución híbrida** compuesta por tres elementos:

1. **LLM instruccional** para generar respuestas claras, naturales y empáticas.
2. **Capa de recuperación de información** desde fuentes controladas de EcoMarket, como base de pedidos, catálogo y políticas.
3. **Reglas de negocio y escalamiento humano** para los casos sensibles o inciertos.

En otras palabras, el LLM no respondería “desde memoria” sobre pedidos o políticas, sino que primero recibiría el contexto correcto desde las bases internas de la empresa y luego redactaría la respuesta final para el cliente.

## 3. ¿Por qué una solución híbrida y no otro enfoque?

### 3.1 Frente a un LLM general sin contexto empresarial

Un modelo general puede redactar bien, pero no es suficiente para este caso porque:

- no conoce de forma nativa el estado real de los pedidos de EcoMarket;
- podría inventar información si no se le entrega contexto confiable;
- no ofrece por sí solo control sobre políticas específicas de devolución, excepciones o restricciones.

Por ello, usar únicamente un LLM de propósito general sería riesgoso para una operación de servicio al cliente.

### 3.2 Frente a un modelo pequeño afinado como única solución

Un modelo pequeño afinado podría ser útil si EcoMarket quisiera optimizar costos o privacidad, pero como única solución también tendría limitaciones:

- requeriría datos históricos suficientemente limpios y representativos;
- podría quedar desactualizado frente a cambios frecuentes en pedidos, inventario o políticas;
- el costo de mantenimiento del fine-tuning puede crecer si la operación cambia rápido.

Por tanto, un modelo pequeño afinado podría ser una mejora futura, pero no lo considero la mejor primera propuesta para este caso.

### 3.3 Ventajas de la solución híbrida

La solución híbrida equilibra mejor las necesidades del problema:

- **precisión** al usar datos internos actualizados;
- **calidad conversacional** gracias al LLM;
- **escalabilidad** para atender gran volumen de consultas repetitivas;
- **control** mediante reglas y derivación a humanos en casos complejos.

## 4. Arquitectura propuesta

La arquitectura propuesta tendría el siguiente flujo:

1. El cliente envía una consulta por chat, correo o red social.
2. Un clasificador ligero identifica la intención principal, por ejemplo: estado del pedido, devolución, información de producto, queja o problema técnico.
3. Si la consulta es de bajo riesgo y puede resolverse automáticamente, el sistema recupera información desde:
   - base de pedidos,
   - catálogo de productos,
   - políticas de devolución.
4. Esa información se entrega como contexto al LLM.
5. El LLM redacta la respuesta siguiendo instrucciones de tono, claridad y límites operativos.
6. Si el caso supera ciertos umbrales de riesgo, se activa el escalamiento a un agente humano.

## 5. Componentes principales

### 5.1 Capa conversacional

Un LLM instruccional encargado de transformar información estructurada en una respuesta útil para el cliente.

### 5.2 Capa de conocimiento empresarial

Fuentes internas confiables:

- estados de pedidos;
- fechas estimadas de entrega;
- enlaces de seguimiento;
- catálogo y atributos del producto;
- políticas de devolución.

### 5.3 Capa de reglas

Reglas para evitar respuestas peligrosas o incorrectas. Ejemplos:

- no inventar fechas si no están disponibles;
- no prometer reembolsos no autorizados;
- no revelar datos personales completos;
- derivar a humano si hay reclamo, fraude, lenguaje agresivo o incidente sensible.

### 5.4 Capa humana

Los agentes humanos no desaparecen. Se enfocan en:

- reclamos complejos;
- clientes molestos o insatisfechos;
- incidentes logísticos delicados;
- excepciones fuera de política;
- retroalimentación para mejorar el sistema.

## 6. Justificación por criterios

### 6.1 Calidad de la respuesta

El LLM aporta redacción natural, coherencia y adaptación del tono. Esto es importante porque el cliente no solo espera un dato, sino una experiencia de atención clara y cordial.

### 6.2 Precisión operativa

La precisión no depende del LLM por sí solo, sino del acceso a información interna. Por eso la capa de recuperación es crítica.

### 6.3 Costo

La solución híbrida evita usar el modelo para “adivinar” información. En vez de eso, usa el LLM principalmente para componer respuestas, lo que puede controlar mejor el costo que un rediseño total basado solo en entrenamiento o fine-tuning desde el inicio.

### 6.4 Escalabilidad

El 80% de consultas repetitivas puede automatizarse con este enfoque. Eso reduce presión sobre el equipo humano y permite atender más clientes en menos tiempo.

### 6.5 Facilidad de integración

La arquitectura es compatible con sistemas reales de e-commerce, porque puede conectarse de forma modular a bases de datos, CRM, sistemas de tickets y catálogos.

### 6.6 Mantenibilidad

Cuando cambie una política o una condición operativa, no siempre será necesario reentrenar el modelo. En muchos casos bastará con actualizar la fuente de datos o la regla correspondiente.

## 7. Alcance esperado de la solución

### Resuelve bien:

- estado del pedido;
- guía de devoluciones según tipo de producto;
- preguntas frecuentes sobre características de productos;
- respuestas iniciales consistentes y disponibles 24/7.

### No debe resolver sola:

- quejas emocionales complejas;
- compensaciones especiales;
- casos de fraude;
- conflictos legales o reputacionales;
- decisiones fuera de política.

## 8. Conclusión

La mejor opción para EcoMarket no es un LLM aislado, sino una **arquitectura híbrida con recuperación de información, reglas de negocio y escalamiento humano**. Esta alternativa responde mejor a las necesidades del caso porque combina precisión operativa con calidad conversacional, reduce el tiempo de respuesta y mantiene control sobre riesgos críticos. Además, ofrece una ruta realista de implementación: empezar con automatización de consultas repetitivas y evolucionar gradualmente hacia una operación más inteligente y robusta.
