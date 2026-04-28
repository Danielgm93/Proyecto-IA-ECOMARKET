# Fase 2: Creación de la Base de Conocimiento de EcoMarket

## 1. Identificación de Documentos

Se identificaron **5 tipos de documentos** cruciales para el sistema de atención al cliente de EcoMarket:

| # | Documento | Formato | Contenido | Justificación |
|---|---|---|---|---|
| 1 | `faq.md` | Markdown | Preguntas frecuentes sobre envíos, pagos, cuenta y sostenibilidad | Cubre el ~60% de consultas repetitivas identificadas en el Taller #1 |
| 2 | `politicas_devolucion.json` | JSON | Reglas de devolución por categoría de producto, plazos y condiciones | Evita respuestas incorrectas sobre elegibilidad de devoluciones (fuente de alucinaciones en el Taller #1) |
| 3 | `pedidos.json` | JSON | Estado actual de pedidos: ID, cliente, producto, estado, fecha | Permite responder consultas de seguimiento en tiempo real sin alucinaciones |
| 4 | `catalogo.json` | JSON | Catálogo de productos: nombre, precio, stock, materiales, certificaciones | Responde preguntas sobre disponibilidad, características y precios |
| 5 | *(extensión futura)* `terminos_servicio.pdf` | PDF | Términos y condiciones, política de privacidad | Para consultas legales y de garantía |

> **Nota:** Los documentos 2 y 3 provienen del Taller #1. El documento 1 y 4 son nuevos para este taller.

---

## 2. Estrategia de Segmentación (Chunking)

### Estrategia seleccionada: **Chunking Recursivo por Caracteres** (`RecursiveCharacterTextSplitter`)

### Parámetros configurados

```python
chunk_size    = 500   # caracteres máximos por chunk
chunk_overlap = 80    # caracteres de solapamiento entre chunks
```

### Por qué esta estrategia es superior para EcoMarket

#### Comparación de estrategias

| Estrategia | Descripción | Problema para EcoMarket |
|---|---|---|
| **Tamaño fijo** | Divide cada N caracteres sin importar el contenido | Puede cortar una política de devolución a la mitad de una condición, generando chunks sin sentido semántico |
| **Por párrafos** | Divide en cada `\n\n` | Algunos párrafos del catálogo tienen 2000+ caracteres; otros tienen 20. Chunks muy desiguales afectan la búsqueda por similitud |
| **Recursivo** ✅ | Intenta separar por párrafos; si el chunk sigue siendo grande, separa por oraciones; si sigue grande, por palabras | Produce chunks coherentes semánticamente, respetando la estructura del documento |

#### Justificación del `chunk_size = 500`

- **Muy pequeño (<200 chars):** Fragmenta el contexto. Un chunk podría decir _"El plazo es de"_ sin completar la información. El modelo no tendría suficiente contexto para responder.
- **Muy grande (>1000 chars):** Cada chunk contiene información de múltiples temas. El embedding del chunk promedia conceptos distintos, reduciendo la precisión de la búsqueda por similitud.
- **500 chars:** Equivale aproximadamente a 2-3 oraciones bien formadas. Suficiente para capturar una política completa o la descripción de un producto, sin mezclar temas.

#### Justificación del `chunk_overlap = 80`

El solapamiento de 80 caracteres (~1 oración corta) garantiza que la **información que aparece en la frontera entre dos chunks** no se pierda. Por ejemplo:

```
Chunk N:   "...El reembolso se procesará en 5-7 días hábiles. Para productos de electrónica,"
Chunk N+1: "Para productos de electrónica, el plazo se extiende a 10 días hábiles..."
```

Sin solapamiento, si un usuario pregunta _"¿Cuánto tarda el reembolso de electrónica?"_, el sistema podría recuperar solo el Chunk N y dar una respuesta incorrecta.

### Estrategia de chunking por tipo de documento

| Documento | Estrategia específica | Razón |
|---|---|---|
| `faq.md` | Recursivo, separando primero por `## ` (headers) | Cada sección de FAQ es una unidad semántica independiente |
| `politicas_devolucion.json` | Convertir a texto estructurado, luego chunking recursivo | Las políticas por categoría deben mantenerse juntas |
| `pedidos.json` | Un chunk por pedido (serialización JSON → string) | Cada pedido es atómico; no tiene sentido dividirlo |
| `catalogo.json` | Un chunk por producto | Cada producto es una unidad semántica completa |

---

## 3. Proceso de Indexación

El proceso de indexación transforma los documentos en bruto en vectores consultables dentro de ChromaDB. Los pasos son:

### Paso 1: Carga de documentos

Cada tipo de documento se carga con el `DocumentLoader` apropiado de LangChain:
- `TextLoader` → para archivos `.md`
- `JSONLoader` → para archivos `.json`, extrayendo campos relevantes con `jq_schema`

### Paso 2: Chunking

Se aplica `RecursiveCharacterTextSplitter` con los parámetros definidos. Cada chunk hereda **metadata** del documento original:
- `source`: nombre del archivo de origen
- `tipo_doc`: categoría (faq, politica, pedido, catalogo)
- `chunk_id`: índice del chunk dentro del documento

Esta metadata es fundamental para el **filtrado selectivo**: si un usuario pregunta por un pedido específico, el sistema puede limitar la búsqueda solo a los chunks de tipo `pedido`.

### Paso 3: Generación de embeddings

El modelo `paraphrase-multilingual-MiniLM-L12-v2` convierte cada chunk de texto en un vector de 384 dimensiones. Este vector captura el significado semántico del texto en el espacio vectorial.

```
"¿Política de devolución para electrodomésticos?" 
    → [0.23, -0.45, 0.12, ..., 0.67]  ← vector de 384 dimensiones
```

### Paso 4: Almacenamiento en ChromaDB

Los vectores, junto con el texto original y la metadata, se almacenan en ChromaDB usando un índice **HNSW (Hierarchical Navigable Small World)**, que permite búsquedas por similitud coseno en tiempo sub-lineal.

### Flujo de consulta (en tiempo real)

```
Pregunta del usuario
        │
        ▼
   [Embedding de la pregunta]  → vector_q
        │
        ▼
   [ChromaDB: similitud coseno(vector_q, todos los chunks)]
        │
        ▼
   [Top-K chunks más similares recuperados] (K=4 por defecto)
        │
        ▼
   [Construcción del prompt enriquecido]
   "Contexto: {chunk1}\n{chunk2}\n..."
   "Pregunta: {pregunta del usuario}"
        │
        ▼
   [LLM genera respuesta basada SOLO en el contexto]
```

Este flujo garantiza que **el LLM nunca inventa información**: si la respuesta no está en los chunks recuperados, el sistema instruyó al modelo para responder _"No tengo información suficiente para responder esta consulta"_.
