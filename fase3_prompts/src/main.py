from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

# ---------------------------------------------------------------------------
# Provider configuration
#
# Set the PROVIDER environment variable to choose the backend:
#   "ollama"   — local Ollama instance (default, sin costo)
#   "groq"     — Groq Cloud API (capa gratuita generosa, recomendado)
#   "openai"   — OpenAI API (requiere suscripción de pago)
#
# Variables de entorno relevantes por proveedor:
#
#   Ollama:
#     OLLAMA_URL    (default: http://localhost:11434/api/generate)
#     MODEL_NAME    (default: llama3.1)
#
#   Groq:
#     GROQ_API_KEY  (obligatorio) — obtener en https://console.groq.com
#     MODEL_NAME    (default: llama-3.1-8b-instant)
#
#   OpenAI:
#     OPENAI_API_KEY (obligatorio) — obtener en https://platform.openai.com
#     MODEL_NAME     (default: gpt-4o-mini)
# ---------------------------------------------------------------------------

PROVIDER = os.getenv("PROVIDER", "ollama").lower()
MODEL_NAME = os.getenv("MODEL_NAME", "")
TIMEOUT_SECONDS = 120

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

DEFAULT_MODELS = {
    "ollama": "llama3.1",
    "groq": "llama-3.1-8b-instant",
    "openai": "gpt-4o-mini",
}


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class DataLoadError(Exception):
    """Raised when local data files cannot be loaded."""


class ProviderError(Exception):
    """Raised when the LLM provider call fails."""


# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------

def load_json(file_path: Path) -> Any:
    try:
        with file_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError as exc:
        raise DataLoadError(f"No se encontró el archivo: {file_path}") from exc
    except json.JSONDecodeError as exc:
        raise DataLoadError(f"El archivo JSON es inválido: {file_path}") from exc


def find_order(tracking_number: str, orders: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    tracking_normalized = tracking_number.strip().upper()
    for order in orders:
        if order.get("tracking_number", "").upper() == tracking_normalized:
            return order
    return None


def find_policy(product_name: str, policies_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    product_normalized = product_name.strip().lower()
    for policy in policies_data.get("policies", []):
        for example in policy.get("examples", []):
            if example.strip().lower() == product_normalized:
                return policy
    return None


# ---------------------------------------------------------------------------
# Prompt builders
# ---------------------------------------------------------------------------

def build_order_prompt(order: Dict[str, Any]) -> str:
    return f"""
Actúa como un agente de servicio al cliente de EcoMarket.

Tu objetivo es responder de forma amable, clara y profesional.
Usa únicamente la información del contexto. No inventes datos.
Si falta información, dilo explícitamente.
Si el pedido está retrasado, ofrece una disculpa breve y explica la razón del retraso.
No expongas datos sensibles innecesarios.

Contexto del pedido:
- Número de seguimiento: {order['tracking_number']}
- Cliente: {order['customer_name']}
- Producto: {order['product']}
- Estado actual: {order['status']}
- Fecha estimada de entrega: {order['estimated_delivery'] or 'No disponible'}
- Enlace de rastreo: {order['tracking_url']}
- Motivo de retraso: {order['delay_reason'] or 'No aplica'}

Instrucciones de salida:
1. Saluda brevemente.
2. Indica el estado actual del pedido.
3. Menciona la fecha estimada de entrega si está disponible.
4. Incluye el enlace de rastreo.
5. Si el pedido está retrasado, agrega una disculpa y una explicación breve.
6. Cierra ofreciendo ayuda adicional.
""".strip()


def build_return_prompt(
    product_name: str,
    condition: str,
    days_since_purchase: int,
    policy: Optional[Dict[str, Any]],
    default_window_days: int,
) -> str:
    policy_text = "No se encontró una política exacta para este producto."
    if policy is not None:
        policy_text = (
            f"Categoría: {policy['category']}\n"
            f"Devolución permitida: {policy['return_allowed']}\n"
            f"Condición requerida: {policy['required_condition']}\n"
            f"Razón: {policy['reason']}"
        )

    return f"""
Actúa como un agente de servicio al cliente de EcoMarket especializado en devoluciones.

Tu respuesta debe ser clara, empática y útil.
No inventes políticas. Usa únicamente la información del contexto.
Si la devolución no es posible, explícalo con respeto y propone el siguiente paso adecuado.

Contexto del cliente:
- Producto consultado: {product_name}
- Estado del producto: {condition}
- Días desde la compra: {days_since_purchase}
- Ventana general de devolución: {default_window_days} días

Política disponible:
{policy_text}

Instrucciones de salida:
1. Saluda brevemente.
2. Indica si la devolución parece posible o no.
3. Explica la razón de forma simple.
4. Si aplica, menciona la condición del producto y el tiempo transcurrido.
5. Cierra con una recomendación o siguiente paso.
""".strip()


# ---------------------------------------------------------------------------
# LLM provider calls
# ---------------------------------------------------------------------------

def _resolve_model() -> str:
    """Return the model name: env var takes priority, then provider default."""
    return MODEL_NAME or DEFAULT_MODELS.get(PROVIDER, "llama3.1")


def call_ollama(prompt: str) -> str:
    payload = {
        "model": _resolve_model(),
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.2},
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
        return response.json().get("response", "No se recibió respuesta del modelo.").strip()
    except requests.RequestException as exc:
        raise ProviderError(
            "No fue posible conectar con Ollama. "
            "Verifica que el servicio esté activo con: ollama serve"
        ) from exc


def call_openai_compatible(prompt: str, api_url: str, api_key: str, provider_name: str) -> str:
    """Generic call for any OpenAI-compatible API (Groq, OpenAI, etc.)."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": _resolve_model(),
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
    }
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except requests.RequestException as exc:
        raise ProviderError(
            f"Error al conectar con {provider_name}. "
            f"Verifica tu API key y conexión a internet."
        ) from exc
    except (KeyError, IndexError) as exc:
        raise ProviderError(f"Respuesta inesperada de {provider_name}: {exc}") from exc


def call_llm(prompt: str) -> str:
    """Route the prompt to the configured provider."""
    if PROVIDER == "ollama":
        return call_ollama(prompt)

    if PROVIDER == "groq":
        api_key = os.getenv("GROQ_API_KEY", "")
        if not api_key:
            raise ProviderError(
                "Falta la variable de entorno GROQ_API_KEY.\n"
                "Obtén tu clave gratuita en: https://console.groq.com"
            )
        return call_openai_compatible(prompt, GROQ_API_URL, api_key, "Groq")

    if PROVIDER == "openai":
        api_key = os.getenv("OPENAI_API_KEY", "")
        if not api_key:
            raise ProviderError(
                "Falta la variable de entorno OPENAI_API_KEY.\n"
                "Obtén tu clave en: https://platform.openai.com/api-keys"
            )
        return call_openai_compatible(prompt, OPENAI_API_URL, api_key, "OpenAI")

    raise ProviderError(
        f"Proveedor desconocido: '{PROVIDER}'. "
        "Usa uno de: ollama, groq, openai"
    )


# ---------------------------------------------------------------------------
# Query handlers
# ---------------------------------------------------------------------------

def handle_order_query(tracking_number: str) -> str:
    orders = load_json(DATA_DIR / "pedidos.json")
    order = find_order(tracking_number, orders)

    if order is None:
        return (
            "No encontré un pedido con ese número de seguimiento. "
            "Verifica el identificador e inténtalo de nuevo."
        )

    prompt = build_order_prompt(order)
    llm_response = call_llm(prompt)

    return (
        f"=== PROVEEDOR: {PROVIDER.upper()} | MODELO: {_resolve_model()} ===\n\n"
        "=== PROMPT USADO ===\n"
        f"{prompt}\n\n"
        "=== RESPUESTA DEL MODELO ===\n"
        f"{llm_response}"
    )


def handle_return_query(product_name: str, condition: str, days_since_purchase: int) -> str:
    policies_data = load_json(DATA_DIR / "politicas_devolucion.json")
    policy = find_policy(product_name, policies_data)
    default_window_days = int(policies_data.get("window_days_default", 30))

    prompt = build_return_prompt(
        product_name=product_name,
        condition=condition,
        days_since_purchase=days_since_purchase,
        policy=policy,
        default_window_days=default_window_days,
    )
    llm_response = call_llm(prompt)

    return (
        f"=== PROVEEDOR: {PROVIDER.upper()} | MODELO: {_resolve_model()} ===\n\n"
        "=== PROMPT USADO ===\n"
        f"{prompt}\n\n"
        "=== RESPUESTA DEL MODELO ===\n"
        f"{llm_response}"
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def print_help() -> None:
    print("""
Uso:
  python src/main.py pedido <tracking_number>
  python src/main.py devolucion <product_name> <condition> <days_since_purchase>

Ejemplos:
  python src/main.py pedido EM-2026-0003
  python src/main.py devolucion "Cepillo dental de bambú" "sin abrir" 10

Proveedores disponibles (variable de entorno PROVIDER):
  ollama   — modelo local con Ollama (default, sin costo)
  groq     — Groq Cloud, capa gratuita (requiere GROQ_API_KEY)
  openai   — OpenAI API (requiere OPENAI_API_KEY)

Ejemplos con proveedor:
  PROVIDER=groq GROQ_API_KEY=gsk_... python src/main.py pedido EM-2026-0001
  PROVIDER=openai OPENAI_API_KEY=sk-... python src/main.py devolucion "Botella térmica reutilizable 750ml" "nuevo" 5
""".strip())


def main() -> None:
    if len(sys.argv) < 3:
        print_help()
        return

    query_type = sys.argv[1].strip().lower()

    try:
        if query_type == "pedido":
            result = handle_order_query(sys.argv[2])
            print(result)
            return

        if query_type == "devolucion":
            if len(sys.argv) < 5:
                print_help()
                return
            try:
                days_since_purchase = int(sys.argv[4])
            except ValueError:
                raise ValueError("El número de días desde la compra debe ser un entero.")

            result = handle_return_query(sys.argv[2], sys.argv[3], days_since_purchase)
            print(result)
            return

        print_help()

    except (DataLoadError, ProviderError, ValueError) as exc:
        print(f"Error: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
