# Taller Práctico #2 — EcoMarket RAG System

**Curso:** Electiva IV - IA Generativa  
**Estudiantes:** Daniel Garcia - Diana Varela  
**Fecha:** Abril 2026  

## 📌 Descripción

Este repositorio extiende el sistema de atención al cliente de **EcoMarket** desarrollado en el Taller #1, incorporando un sistema **RAG (Retrieval-Augmented Generation)**. A diferencia de los modelos de propósito general, este sistema consulta una base de conocimiento interna antes de generar respuestas, garantizando que la información sobre pedidos, políticas y productos sea precisa, actualizada y libre de alucinaciones.

## 🛠️ Estructura del Repositorio
```text
.
├── README.md                          ← Este archivo con el resumen ejecutivo
├── RESPUESTAS.md                      ← Fase 1 y 2: Justificación técnica y arquitectura
├── Taller2_EcoMarket_RAG_v2.ipynb    ← Notebook principal de ejecución en Google Colab
└── fase3_rag/
    ├── requirements.txt               ← Dependencias (langchain, chromadb, ollama, etc.)
    ├── data/                          ← Base de conocimiento de EcoMarket
    │   ├── faq.md                     ← FAQ de envíos y pagos
    │   ├── politicas_devolucion.json  ← Reglas por categoría de producto
    │   ├── pedidos.json               ← Datos transaccionales de prueba
    │   └── catalogo.json              ← Inventario y precios
    └── src/
        ├── ingest.py                  ← Script de carga e indexación en ChromaDB
        └── rag_ecomarket.py           ← Lógica del chatbot RAG con LangChain


---

## Arquitectura del Sistema RAG

```
El sistema sigue un flujo de procesamiento local para garantizar la privacidad de los datos de los clientes:  
- Ingesta: Los documentos (JSON, MD) se cargan y se dividen mediante RecursiveCharacterTextSplitter.
- Embeddings: Se utiliza el modelo nomic-embed-text a través de Ollama para vectorizar la información.
- Almacenamiento: Los vectores se indexan en ChromaDB (base de datos vectorial local).
- Recuperación: Ante una duda, el sistema busca los fragmentos más similares semánticamente.
- Generación: Se utiliza Llama 3 con un prompt estricto que prohíbe inventar información fuera del contexto.  
```
## Limitaciones y Suposiciones (Rúbrica Fase 3)

De acuerdo con los requerimientos del taller, se detallan las siguientes consideraciones:  

- Infraestructura: El sistema está diseñado para correr localmente mediante Ollama. En entornos como Google Colab, el rendimiento depende de la disponibilidad de GPU; de lo contrario, la latencia de respuesta puede ser alta.
- Persistencia: La base de datos vectorial en este prototipo es volátil en entornos de nube temporal. Para producción, se requeriría un volumen persistente o un servicio como Pinecone.
- Memoria: El asistente actual procesa cada pregunta de forma independiente (stateless). No mantiene historial de la conversación previa.
- Suposición de Veracidad: Se asume que los archivos en la carpeta /data son la única fuente de verdad. Si un dato no existe allí, el modelo está instruido para responder: "Lo siento, no tengo las herramientas para atender su solicitud"[cite: 1, 2].
---
---

## Ejecución rápida (Google Colab)
1. Sube el archivo Taller2_EcoMarket_RAG_v2.ipynb a Google Colab.
2. Asegúrate de que la carpeta /data esté cargada o vinculada desde este repositorio.
3. Ejecuta las celdas en orden para instalar Ollama, descargar modelos e iniciar el chatbot.
