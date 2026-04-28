# Fase 3 — Código RAG: Instrucciones de Ejecución

## Requisitos

- Python 3.10 o superior
- ~1 GB de espacio en disco (modelo de embeddings ~500 MB + ChromaDB)
- Conexión a internet para la primera ejecución (descarga del modelo)

## Instalación

```bash
cd fase3_rag
pip install -r requirements.txt
```

## Paso 1: Indexar la base de conocimiento

Este paso carga todos los documentos de `data/`, los divide en chunks y los almacena como vectores en ChromaDB.

```bash
python src/ingest.py
```

**Salida esperada:**
```
=======================================================
  EcoMarket RAG — Indexación de la base de conocimiento
=======================================================

[+] Creando nueva base de datos vectorial...

[1/3] Cargando y segmentando documentos...
  FAQ:        24 chunks generados
  Políticas:  8 chunks generados
  Pedidos:    10 chunks generados
  Catálogo:   10 chunks generados

  Total chunks: 52

[2/3] Cargando modelo de embeddings: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
  (La primera ejecución descarga el modelo ~500MB — puede tardar unos minutos)

[3/3] Generando vectores y almacenando en ChromaDB...

=======================================================
  ✅ Indexación completada.
  Base de datos guardada en: fase3_rag/chroma_db
  Total de vectores almacenados: 52
=======================================================
```

> ⚠️ Solo necesitas ejecutar `ingest.py` una vez. Vuelve a ejecutarlo si modificas los archivos en `data/`.

---

## Paso 2: Ejecutar el chatbot RAG

### Opción A — Con Groq (gratuito, recomendado)

1. Regístrate en [console.groq.com](https://console.groq.com) (gratuito)
2. Crea una API key
3. Ejecuta:

```bash
export GROQ_API_KEY=gsk_tu_clave_aqui
python src/rag_ecomarket.py
```

### Opción B — Con Ollama (100% local, sin costo, sin internet)

```bash
# Instalar Ollama: https://ollama.com
ollama pull llama3.1
ollama serve

# En otra terminal:
python src/rag_ecomarket.py --provider ollama
```

---

## Opciones de ejecución

```bash
# Modo interactivo (por defecto)
python src/rag_ecomarket.py

# Modo verbose: muestra los chunks recuperados en cada consulta
python src/rag_ecomarket.py --verbose

# Modo no interactivo: responde una sola pregunta
python src/rag_ecomarket.py --pregunta "¿Cuánto tarda el envío estándar?"

# Cambiar proveedor de LLM
python src/rag_ecomarket.py --provider ollama
```

---

## Ejemplos de consultas para probar el sistema

```
¿Cuánto tarda el envío estándar?
¿Puedo devolver un shampoo sólido que ya abrí?
¿Cuál es el estado del pedido EM-2026-0003?
¿Tienen cargadores solares? ¿Cuánto cuestan?
¿Qué son los EcoCoins?
¿Pueden enviar a Pasto?
¿Qué hago si recibí un producto dañado?
¿Cuánto cuesta devolver un producto por cambio de opinión?
```

---

## Limitaciones y Supuestos

### Limitaciones

1. **Modelo de embeddings en CPU:** El modelo `paraphrase-multilingual-MiniLM-L12-v2` se ejecuta en CPU, lo que hace la primera carga más lenta (~15-30 segundos). En producción se recomendaría una GPU para acelerar el proceso.

2. **Base de datos de pedidos estática:** Los pedidos en `data/pedidos.json` son datos de prueba estáticos. En un sistema real, esta información vendría de la base de datos en tiempo real de EcoMarket (PostgreSQL, MongoDB, etc.), lo que requeriría un conector adicional.

3. **Sin memoria conversacional:** El sistema no recuerda el historial de la conversación. Cada pregunta se procesa de forma independiente. Para implementar memoria habría que usar `ConversationBufferMemory` de LangChain.

4. **Sin autenticación de cliente:** El sistema no verifica la identidad del cliente antes de mostrar información de pedidos. En producción esto sería un requerimiento de seguridad crítico.

5. **TOP_K fijo en 4:** El número de chunks recuperados es fijo. Para consultas muy específicas (ej. un ID de pedido) podría ser suficiente con 1; para consultas complejas podrían necesitarse más. Una mejora futura sería el retrieval adaptativo.

### Supuestos

- Se asume que el servidor tiene acceso a internet para la primera descarga del modelo de embeddings (~500 MB).
- Se asume Python 3.10+ disponible en el entorno de ejecución.
- Para la opción Groq, se asume una cuenta activa con cuota gratuita disponible (límite: 14,400 solicitudes/día en el tier gratuito).
- Los documentos en `data/` representan el estado real del sistema EcoMarket para propósitos de prueba.
