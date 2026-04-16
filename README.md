# Taller Práctico #1 — EcoMarket

**Curso:** Electiva IV - IA Generativa  
**Estudiante:** Daniel Garcia - Diana Varela   
**Fecha:** Abril 2026  

---

## Descripción

Este repositorio contiene la solución completa del Taller Práctico #1, cuyo caso de estudio es la optimización del servicio de atención al cliente de **EcoMarket**, una empresa de comercio electrónico de productos sostenibles.

La solución se organiza en tres fases:

| Fase | Archivo | Descripción |
|------|---------|-------------|
| 1 | `fase1_modelo.md` | Selección y justificación del modelo de IA |
| 2 | `fase2_analisis.md` | Fortalezas, limitaciones y riesgos éticos |
| 3 | `fase3_prompts/` | Implementación práctica de ingeniería de prompts |

---

## Estructura del repositorio

```text
.
├── README.md                          ← Este archivo
├── fase1_modelo.md                    ← Fase 1: justificación del modelo
├── fase2_analisis.md                  ← Fase 2: análisis crítico
└── fase3_prompts/
    ├── README.md                      ← Instrucciones detalladas de ejecución
    ├── requirements.txt               ← Dependencias Python
    ├── data/
    │   ├── pedidos.json               ← Base de datos de prueba (10 pedidos)
    │   └── politicas_devolucion.json  ← Políticas de devolución por categoría
    └── src/
        └── main.py                    ← Script principal con soporte multi-proveedor
```

---

## Resumen de la propuesta (Fase 1)

Para resolver el cuello de botella de EcoMarket se propone una **arquitectura híbrida** compuesta por:

- un **LLM instruccional** que redacta respuestas naturales, claras y empáticas;
- una **capa de recuperación de información** que consulta datos reales de pedidos, catálogo y políticas antes de generar la respuesta;
- **reglas de negocio** que previenen alucinaciones e impiden respuestas fuera de política;
- un **mecanismo de escalamiento humano** para casos complejos, quejas o situaciones de riesgo.

Esta arquitectura responde directamente al perfil de consultas de EcoMarket: el 80 % son repetitivas y automatizables; el 20 % restante requiere intervención humana.

---

## Ejecución rápida (Fase 3)

El script soporta tres proveedores. Ver instrucciones completas en [`fase3_prompts/README.md`](fase3_prompts/README.md).

**Con Groq (gratuito, recomendado):**

```bash
cd fase3_prompts
pip install -r requirements.txt

export PROVIDER=groq
export GROQ_API_KEY=gsk_tu_clave_aqui   # Obtener en https://console.groq.com

python src/main.py pedido EM-2026-0003
python src/main.py devolucion "Cepillo dental de bambú" "sin abrir" 10
```

**Con Ollama (local, sin costo):**

```bash
ollama pull llama3.1
ollama serve

cd fase3_prompts
pip install -r requirements.txt
python src/main.py pedido EM-2026-0003
```

**Con OpenAI (de pago):**

```bash
export PROVIDER=openai
export OPENAI_API_KEY=sk-tu_clave_aqui
python src/main.py pedido EM-2026-0001
```

