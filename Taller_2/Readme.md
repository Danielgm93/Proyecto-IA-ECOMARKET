# Taller Práctico #2 — EcoMarket RAG System

**Curso:** Electiva IV - IA Generativa  
**Estudiante:** Daniel Garcia - Diana Varela  
**Fecha:** Abril 2026

---

## Descripción

Este repositorio extiende el sistema de atención al cliente de **EcoMarket** desarrollado en el Taller #1, incorporando un sistema **RAG (Retrieval-Augmented Generation)** que permite al modelo consultar una base de conocimiento interna antes de generar respuestas. Esto elimina las alucinaciones y garantiza respuestas precisas, actualizadas y contextualizadas.

---

## Estructura del repositorio

```
.
├── README.md                          ← Este archivo
├── fase1_componentes.md               ← Fase 1: Selección y justificación de componentes RAG
├── fase2_base_conocimiento.md         ← Fase 2: Creación de la base de conocimiento
└── fase3_rag/
    ├── README.md                      ← Instrucciones detalladas de ejecución
    ├── requirements.txt               ← Dependencias Python
    ├── data/
    │   ├── faq.md                     ← Preguntas frecuentes de EcoMarket
    │   ├── politicas_devolucion.json  ← Políticas de devolución por categoría
    │   ├── pedidos.json               ← Base de datos de pedidos (heredada del Taller 1)
    │   └── catalogo.json              ← Catálogo de productos de EcoMarket
    └── src/
        ├── ingest.py                  ← Carga, chunking e indexación de documentos
        └── rag_ecomarket.py           ← Sistema RAG principal (atención al cliente)
```

---

## Arquitectura del Sistema RAG

```
Usuario
   │
   ▼
[Pregunta del cliente]
   │
   ▼
[Modelo de Embeddings: multilingual-MiniLM-L12-v2]
   │  Convierte la pregunta en vector
   ▼
[ChromaDB: Búsqueda por similitud coseno]
   │  Recupera los K chunks más relevantes
   ▼
[Prompt enriquecido con contexto real]
   │
   ▼
[LLM: Groq/llama3-8b-8192 o Ollama/llama3.1]
   │  Genera respuesta fundamentada
   ▼
[Respuesta al cliente]
```

---

## Ejecución rápida

Ver instrucciones completas en [`fase3_rag/README.md`](fase3_rag/README.md).

```bash
cd fase3_rag
pip install -r requirements.txt

# Paso 1: Indexar documentos (solo la primera vez)
python src/ingest.py

# Paso 2: Iniciar el chatbot RAG
export GROQ_API_KEY=gsk_tu_clave_aqui
python src/rag_ecomarket.py
```
