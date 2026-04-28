# Fase 1: Selección y Justificación de Componentes del Sistema RAG

## 1. Modelo de Embeddings

### Selección: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`

**Proveedor:** Hugging Face (código abierto)  
**Dimensión del vector:** 384  
**Idiomas soportados:** 50+ idiomas, incluido español de forma nativa  
**Licencia:** Apache 2.0 (uso comercial permitido)

### Justificación

| Factor | Evaluación |
|---|---|
| **Soporte para español** | ⭐⭐⭐⭐⭐ — Entrenado explícitamente en corpus multilingüe (incluye español latinoamericano). Captura matices semánticos como "devolución" ≈ "reembolso" ≈ "retorno". |
| **Costo** | ⭐⭐⭐⭐⭐ — Completamente gratuito. Se ejecuta localmente, sin llamadas a API externas. Ideal para EcoMarket que está en etapa de crecimiento y necesita controlar costos. |
| **Rendimiento** | ⭐⭐⭐⭐ — Modelo MiniLM optimizado para velocidad. En hardware modesto (CPU), procesa ~1000 frases/segundo. Suficiente para el volumen de EcoMarket. |
| **Facilidad de uso** | ⭐⭐⭐⭐⭐ — Integración directa con LangChain vía `HuggingFaceEmbeddings`. Sin configuración adicional. |
| **Privacidad** | ⭐⭐⭐⭐⭐ — Los datos de clientes (pedidos, correos) nunca salen del servidor de EcoMarket. |

### Alternativas Consideradas y Descartadas

**`text-embedding-3-small` (OpenAI)**
- ✅ Alta precisión en español
- ❌ Costo por token (~$0.02 / millón de tokens). Con el volumen proyectado de EcoMarket, el costo mensual sería significativo.
- ❌ Los datos de clientes se envían a servidores externos → riesgo de privacidad.

**`embed-multilingual-v3.0` (Cohere)**
- ✅ Excelente para multilingüe
- ❌ Modelo propietario con tier gratuito limitado a 100 llamadas/minuto.
- ❌ Dependencia de un proveedor externo = riesgo operacional.

**`all-MiniLM-L6-v2` (Sentence Transformers)**
- ✅ Muy rápido y ligero
- ❌ Entrenado principalmente en inglés. Para consultas en español como _"¿Cuándo llega mi pedido?"_, su rendimiento es notablemente inferior al modelo multilingüe seleccionado.

### Conclusión

El modelo `paraphrase-multilingual-MiniLM-L12-v2` representa el mejor balance entre **rendimiento en español**, **costo cero** y **privacidad de datos** para el contexto de EcoMarket.

---

## 2. Base de Datos Vectorial

### Selección: `ChromaDB`

**Tipo:** Embebida (in-process), open source  
**Licencia:** Apache 2.0  
**Persistencia:** Disco local (SQLite + HNSW index)

### Justificación

| Factor | ChromaDB ✅ | Pinecone | Weaviate |
|---|---|---|---|
| **Costo** | Gratuito, local | Free tier muy limitado (1 índice, 100k vectores). Plan de pago desde $70/mes | Gratuito en self-hosted; cloud tiene costo |
| **Escalabilidad** | Hasta ~1M vectores en modo local; cluster en producción | Excelente escalabilidad serverless | Excelente, pero requiere más infraestructura |
| **Facilidad de uso** | `pip install chromadb` + 5 líneas de código | Requiere cuenta, API key, configuración de índices | Requiere Docker o cuenta cloud; curva de aprendizaje alta |
| **Integración LangChain** | ✅ Nativa y documentada | ✅ Nativa | ✅ Nativa |
| **Soporte español / metadata** | ✅ Filtrado por metadata (categoría, tipo_doc) | ✅ Con filtros de metadata | ✅ Con schema personalizado |
| **Dependencia externa** | ❌ Ninguna (corre en el mismo proceso) | ❌ Alta (API Pinecone) | ⚠️ Media (Docker o cloud) |

### Análisis para el Caso EcoMarket

EcoMarket es una empresa en crecimiento con una base de conocimiento de tamaño moderado (~500 documentos / chunks iniciales). Sus necesidades actuales son:

1. **Iteración rápida**: El equipo necesita actualizar documentos frecuentemente (nuevas políticas, productos). ChromaDB permite re-indexar sin configuración externa.
2. **Sin infraestructura adicional**: No hay presupuesto para servicios cloud en esta fase.
3. **Privacidad**: Los datos de pedidos y clientes son sensibles. Mantenerlos en un servidor propio elimina el riesgo de filtración.

**Para una fase de escalamiento** (millones de documentos, múltiples regiones), la migración a **Pinecone** o **Weaviate Cloud** sería recomendable. La ventaja de ChromaDB es que LangChain abstrae la capa de vector store, haciendo esta migración futura prácticamente transparente a nivel de código.

### Alternativas Descartadas

**Pinecone**
- ✅ Excelente para producción a escala masiva
- ❌ Requiere cuenta externa y API key
- ❌ El tier gratuito expira y los datos residen en servidores de Pinecone
- ❌ Overkill para el volumen actual de EcoMarket

**Weaviate**
- ✅ Potente con búsqueda híbrida (vectorial + keyword)
- ❌ Requiere Docker para uso local, añadiendo complejidad operacional innecesaria en esta etapa
- ❌ Curva de aprendizaje más pronunciada para el equipo de EcoMarket

### Conclusión

**ChromaDB** es la opción óptima para EcoMarket en esta fase: costo cero, instalación trivial, integración nativa con LangChain y suficiente capacidad para la base de conocimiento proyectada. La arquitectura está diseñada para migrar a Pinecone o Weaviate en el futuro sin reescribir el sistema.
