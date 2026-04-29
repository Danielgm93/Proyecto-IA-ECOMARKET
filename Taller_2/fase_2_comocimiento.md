## Fase 2: Base de Conocimiento y Segmentación
1. **Identificación de Documentos**
Se integraron 4 fuentes de datos críticas en formatos diversos para cubrir todas las necesidades del cliente:  

- faq.md: Preguntas frecuentes sobre pagos y envíos (Markdown).  

- politicas_devolucion.json: Reglas estructuradas por categoría de producto.  

- pedidos.json: Datos transaccionales para consultas de estado de envío.  

- catalogo.json: Información técnica, precios y stock de productos

## 2. Estrategia de Segmentación (Chunking)
**Técnica:** RecursiveCharacterTextSplitter.  

**Configuración:** chunk_size=500 y chunk_overlap=80.  

**Justificación:** Esta estrategia evita cortar oraciones a la mitad al intentar respetar la estructura del texto (párrafos, oraciones). El solapamiento (overlap) de 80 caracteres asegura que no se pierda el contexto semántico entre fragmentos adyacentes, lo cual es vital para que el modelo entienda condiciones de devolución complejas.

## Fase 3: Integración y Limitaciones del Sistema
1. Implementación del CódigoEl sistema utiliza el lenguaje de expresión de LangChain (LCEL) para conectar el Retriever (ChromaDB), el Prompt estructurado y el LLM (Llama 3 vía Ollama).
   - Regla de Oro: Se implementó un "System Prompt" con reglas estrictas que obligan al modelo a responder únicamente con el contexto recuperado, mitigando alucinaciones.
   
3. Limitaciones y SuposicionesPara la evaluación de esta fase, se detallan las siguientes limitaciones técnicas del prototipo:  Persistencia de Datos: Al ejecutarse en Google Colab, la base de datos y los modelos de Ollama son volátiles y deben re-indexarse en cada sesión.
   - Hardware: La velocidad de respuesta depende directamente de la potencia de la CPU/GPU asignada, lo que puede generar latencias en la generación de texto.
   - Memoria Conversacional: El prototipo actual no tiene memoria de corto plazo; cada consulta se trata de forma independiente sin recordar el historial del chat.
   - Suposición de Datos: Se asume que los archivos JSON en el repositorio representan la verdad única de la empresa para efectos de esta prueba.
