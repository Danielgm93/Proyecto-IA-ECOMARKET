# Fase 1: Selección y Justificación de Componentes del Sistema RAG

## 1. Modelo de Embeddings

### Selección: nomic-embed-text (vía Ollama)

### Justificación: 
Se seleccionó este modelo por su alta eficiencia y rendimiento en tareas de recuperación de información. Al ejecutarse localmente a través de Ollama, garantiza costo cero y privacidad total, ya que los datos de la empresa nunca salen del entorno de ejecución.  

- Soporte para español: Aunque es un modelo compacto, demuestra una alta capacidad para capturar relaciones semánticas en español, fundamental para entender consultas sobre "reembolsos" o "devoluciones".  

- Alternativa descartada: Se evaluó text-embedding-3-small de OpenAI, pero se descartó para evitar la dependencia de APIs pagas y el envío de datos sensibles a servidores externos.

## 2. Base de Datos Vectorial

## Selección: ChromaDB  

## Justificación: 
Es una base de datos vectorial de código abierto que permite el almacenamiento local (embebido). Es ideal para EcoMarket porque no requiere infraestructura adicional y se integra de forma nativa con LangChain.  Escalabilidad: Permite manejar miles de fragmentos de información con latencias mínimas, permitiendo búsquedas por similitud rápidas incluso en hardware modesto.  
