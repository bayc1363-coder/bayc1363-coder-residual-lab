"""UI/CLI model catalog for equal-resolution chat (research-only)."""

from __future__ import annotations

import json
import os
from typing import Any

from residual_lab.paths import models_catalog_path

EXPERIENTIAL_BASE_URL = "https://api.experientiallabs.ai/v1"
OTHER_CHOICE = "other"
API_KEY_ENV_NAMES = ("EXPLABS_API_KEY", "RESIDUAL_LAB_API_KEY", "OPENAI_API_KEY")

_FALLBACK_MODELS: tuple[dict[str, str], ...] = (
    {"id": "mock", "label": "mock — offline stub (no key)", "tier": "offline"},
    {"id": "other", "label": "Other… (type id below)", "tier": "custom"},
)


def load_catalog() -> dict[str, Any]:
    path = models_catalog_path()
    if not path.is_file():
        return {
            "default_base_url": EXPERIENTIAL_BASE_URL,
            "models": [dict(m) for m in _FALLBACK_MODELS],
        }
    data = json.loads(path.read_text(encoding="utf-8"))
    models = [m for m in (data.get("models") or []) if isinstance(m, dict) and m.get("id")]
    ids = {str(m["id"]) for m in models}
    if "mock" not in ids:
        models.insert(0, dict(_FALLBACK_MODELS[0]))
    if "other" not in ids:
        models.append(dict(_FALLBACK_MODELS[1]))
    data["models"] = models
    data.setdefault("default_base_url", EXPERIENTIAL_BASE_URL)
    return data


def catalog_models() -> list[dict[str, Any]]:
    return list(load_catalog()["models"])


def catalog_ids() -> tuple[str, ...]:
    return tuple(str(m["id"]) for m in catalog_models())


def selector_choices() -> list[tuple[str, str]]:
    """Gradio dropdown: (label, value/id)."""
    return [(str(m.get("label") or m["id"]), str(m["id"])) for m in catalog_models()]


def catalog_entry(model_id: str) -> dict[str, Any] | None:
    mid = (model_id or "").strip()
    for item in catalog_models():
        if str(item.get("id")) == mid:
            return item
    return None


def resolve_model_id(choice: str, custom: str = "") -> str:
    picked = (choice or "").strip() or "mock"
    if picked in {OTHER_CHOICE, "Other…"}:
        mid = (custom or "").strip()
        if not mid:
            raise RuntimeError("Type a model id in the Other… box, or pick a catalog model.")
        return mid
    return picked


def is_mock_model(model_id: str) -> bool:
    return (model_id or "").strip().lower() in {"", "mock", "offline"}


def catalog_default_base_url() -> str:
    url = str(load_catalog().get("default_base_url") or EXPERIENTIAL_BASE_URL).strip()
    return url.rstrip("/") or EXPERIENTIAL_BASE_URL


def default_base_url(model_id: str, explicit: str = "") -> str:
    if is_mock_model(model_id):
        return ""
    url = (explicit or "").strip()
    if url:
        return url.rstrip("/")
    entry = catalog_entry(model_id)
    if entry and str(entry.get("base_url") or "").strip():
        return str(entry["base_url"]).strip().rstrip("/")
    env = (os.environ.get("RESIDUAL_LAB_BASE_URL") or "").strip()
    if env:
        return env.rstrip("/")
    return catalog_default_base_url()


def api_key_env_for_model(model_id: str, api_key_env: str = "") -> str:
    entry = catalog_entry(model_id)
    if entry and str(entry.get("api_key_env") or "").strip():
        return str(entry["api_key_env"]).strip()
    return (api_key_env or "").strip()


def api_key_from_env(api_key_env: str = "") -> tuple[str, str]:
    """Return (key, env_name). Never log the key. Empty key means fail closed."""
    names: list[str] = []
    for name in (*API_KEY_ENV_NAMES, api_key_env):
        n = (name or "").strip()
        if n and n not in names:
            names.append(n)
    for name in names:
        val = os.environ.get(name, "")
        if val.strip():
            return val.strip(), name
    return "", ""


def missing_key_message(model_id: str) -> str:
    return (
        f"Live model `{model_id}` needs EXPLABS_API_KEY or RESIDUAL_LAB_API_KEY "
        "in the environment (never paste a key into the UI). Pick **mock** to test offline."
    )
