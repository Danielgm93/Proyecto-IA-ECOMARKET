# Fase 3 — Ingeniería de prompts

Esta carpeta implementa los dos ejercicios prácticos del taller usando IA generativa real:

1. **Consulta de estado de pedido** — el modelo responde con el estado actual, fecha estimada y enlace de rastreo.
2. **Guía de devolución** — el modelo determina si un producto puede devolverse según la política de EcoMarket y explica el motivo.

---

## Cómo funciona

```
Consulta del usuario
       ↓
Búsqueda en datos locales (JSON)
       ↓
Construcción del prompt (rol + contexto + restricciones + instrucciones)
       ↓
Llamada al LLM (Ollama / Groq / OpenAI)
       ↓
Respuesta empática al cliente
```

Los datos nunca los inventa el modelo. Se recuperan primero desde los archivos JSON y se inyectan como contexto en el prompt, reduciendo el riesgo de alucinaciones.

---

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `data/pedidos.json` | 10 pedidos de prueba con estados variados (en tránsito, retrasado, entregado, cancelado) |
| `data/politicas_devolucion.json` | Políticas por categoría: accesorios, higiene personal, cosmética, consumibles, hogar |
| `src/main.py` | Script principal. Soporta Ollama, Groq y OpenAI mediante variable de entorno |
| `requirements.txt` | Única dependencia: `requests` |

---

## Instalación

Requiere Python 3.10 o superior.

```bash
cd fase3_prompts
pip install -r requirements.txt
```

---

## Proveedores soportados

Selecciona el proveedor con la variable de entorno `PROVIDER` (por defecto: `ollama`).

| `PROVIDER` | Requiere | Costo | Modelo por defecto |
|------------|----------|-------|--------------------|
| `ollama` | Ollama instalado localmente | Sin costo | `llama3.1` |
| `groq` | `GROQ_API_KEY` | **Gratuito** (capa free) | `llama-3.1-8b-instant` |
| `openai` | `OPENAI_API_KEY` | De pago | `gpt-4o-mini` |

Para cambiar el modelo independientemente del proveedor, usa `MODEL_NAME`:

```bash
MODEL_NAME=llama-3.3-70b-versatile PROVIDER=groq GROQ_API_KEY=gsk_... python src/main.py pedido EM-2026-0001
```

---

## Ejecución por proveedor

### Opción A — Ollama (local, sin costo)

1. Instalar Ollama desde [ollama.com](https://ollama.com)
2. Descargar el modelo y levantar el servidor:

```bash
ollama pull llama3.1
ollama serve
```

3. Ejecutar:

```bash
python src/main.py pedido EM-2026-0003
python src/main.py devolucion "Cepillo dental de bambú" "sin abrir" 10
```

---

### Opción B — Groq (gratuito, recomendado)

Groq ofrece una capa gratuita generosa, sin necesidad de instalar nada localmente.

1. Crear cuenta en [console.groq.com](https://console.groq.com)
2. Generar una API key
3. Ejecutar:

**Linux / macOS:**
```bash
export PROVIDER=groq
export GROQ_API_KEY=gsk_tu_clave_aqui
python src/main.py pedido EM-2026-0003
python src/main.py devolucion "Cepillo dental de bambú" "sin abrir" 10
```

**Windows (CMD):**
```cmd
set PROVIDER=groq
set GROQ_API_KEY=gsk_tu_clave_aqui
python src/main.py pedido EM-2026-0003
python src/main.py devolucion "Cepillo dental de bambú" "sin abrir" 10
```

---

### Opción C — OpenAI (de pago)

```bash
export PROVIDER=openai
export OPENAI_API_KEY=sk-tu_clave_aqui
python src/main.py pedido EM-2026-0001
python src/main.py devolucion "Botella térmica reutilizable 750ml" "nuevo" 5
```

---

## Ejemplos de uso completos

```bash
# Pedido en tránsito
python src/main.py pedido EM-2026-0001

# Pedido retrasado (el modelo incluye disculpa y explicación)
python src/main.py pedido EM-2026-0003

# Pedido cancelado
python src/main.py pedido EM-2026-0010

# Devolución NO permitida (higiene personal)
python src/main.py devolucion "Cepillo dental de bambú" "sin abrir" 10

# Devolución SÍ permitida (accesorio en buen estado, dentro del plazo)
python src/main.py devolucion "Botella térmica reutilizable 750ml" "como nuevo" 5

# Devolución negada por tiempo (fuera de la ventana de 30 días)
python src/main.py devolucion "Kit de cubiertos reutilizables" "sin abrir" 45
```

---

## Diseño de los prompts

### Prompt 1 — estado del pedido

El prompt le asigna al modelo el **rol** de agente de EcoMarket y le entrega el contexto completo del pedido como datos estructurados. Las instrucciones clave son:

- "Usa únicamente la información del contexto. No inventes datos." → previene alucinaciones.
- "Si el pedido está retrasado, ofrece una disculpa breve y explica la razón." → manejo de casos negativos.
- Instrucciones de salida numeradas → garantizan una respuesta consistente y completa.
- Temperatura 0.2 → respuestas predecibles y controladas.

### Prompt 2 — devolución de producto

El prompt inyecta la política específica del producto (recuperada del JSON) antes de que el modelo responda. Esto significa que el modelo nunca decide por su cuenta si algo es devolvible; solo redacta la respuesta basándose en la política entregada. Las instrucciones clave son:

- "No inventes políticas." → la decisión ya viene del sistema, no del modelo.
- "Si la devolución no es posible, explícalo con respeto y propone el siguiente paso." → mantiene el tono empático incluso en respuestas negativas.
- Distinción explícita entre productos de higiene, consumibles y accesorios → cubre el desafío planteado por el taller.

---

## Evidencias de ejecución

La carpeta `outputs/` contiene los resultados de ejecuciones reales con Groq, cubriendo los casos más representativos del taller:

| Archivo | Caso cubierto |
|---------|---------------|
| `pedido_en_transito.txt` | Estado normal, entrega próxima |
| `pedido_retrasado.txt` | Retraso logístico con disculpa y explicación |
| `pedido_cancelado.txt` | Cancelación por pago no confirmado |
| `devolucion_aprobada.txt` | Accesorio en buen estado dentro del plazo |
| `devolucion_negada_higiene.txt` | Producto de higiene personal (no devolvible por política) |
| `devolucion_negada_tiempo.txt` | Accesorio fuera de la ventana de 30 días |

---

## Estructura del output

Cada ejecución imprime tres secciones:

```
=== PROVEEDOR: GROQ | MODELO: llama-3.1-8b-instant ===

=== PROMPT USADO ===
[El prompt completo enviado al modelo]

=== RESPUESTA DEL MODELO ===
[La respuesta generada]
```

Esto permite verificar exactamente qué se le envió al modelo y qué respondió, facilitando la evaluación del impacto de la ingeniería de prompts.
