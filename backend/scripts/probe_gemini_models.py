#!/usr/bin/env python3
"""Prueba aislada para detectar modelos Gemini accesibles en este entorno.

Uso:
  python scripts/probe_gemini_models.py
  python scripts/probe_gemini_models.py --update-env --env-file ../.env
"""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path

from google import genai
from google.genai import types

CHAT_CANDIDATES = [
    "gemini-2.0-flash",
    "gemini-2.5-flash",
    "gemini-1.5-flash",
    "gemini-1.5-flash-latest",
    "gemini-1.5-pro",
    "gemini-1.5-pro-latest",
]

EMBEDDING_CANDIDATES = [
    "text-embedding-004",
    "models/text-embedding-004",
    "gemini-embedding-001",
    "models/gemini-embedding-001",
    "models/embedding-001",
]

EMBEDDING_DIMENSIONALITY = 3072

ENV_KEY_PATTERN = re.compile(
    r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)\s*$"
)


def model_aliases(model_name: str) -> list[str]:
    clean_name = (model_name or "").strip()
    if not clean_name:
        return []

    aliases = [clean_name]
    if clean_name.startswith("models/"):
        aliases.append(clean_name[len("models/") :])
    else:
        aliases.append(f"models/{clean_name}")

    seen: set[str] = set()
    ordered: list[str] = []
    for alias in aliases:
        if alias not in seen:
            seen.add(alias)
            ordered.append(alias)

    return ordered


def dedupe_models(models: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for model_name in models:
        for alias in model_aliases(model_name):
            if alias not in seen:
                seen.add(alias)
                ordered.append(alias)
    return ordered


def parse_env_file(env_file: Path) -> dict[str, str]:
    if not env_file.exists():
        return {}

    parsed: dict[str, str] = {}
    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        match = ENV_KEY_PATTERN.match(raw_line)
        if not match:
            continue

        key = match.group(1)
        value = match.group(2).strip()

        if value and value[0] in {'"', "'"} and value[-1] == value[0]:
            value = value[1:-1]
        else:
            # Quita comentarios inline solo para valores no entrecomillados.
            value = value.split(" #", 1)[0].strip()

        parsed[key] = value

    return parsed


def resolve_env_path(env_file_arg: str) -> Path:
    candidate = Path(env_file_arg).expanduser()
    if candidate.is_absolute():
        return candidate

    # Prioriza la ruta relativa al directorio de ejecucion actual.
    cwd_resolved = (Path.cwd() / candidate).resolve()
    if cwd_resolved.exists():
        return cwd_resolved

    # Fallback: relativo al archivo del script.
    script_resolved = (Path(__file__).resolve().parent / candidate).resolve()
    if script_resolved.exists():
        return script_resolved

    # Si no existe aun, usa la ruta relativa al cwd para permitir creacion/actualizacion.
    return cwd_resolved


def get_gemini_api_key(env_file: Path) -> tuple[str | None, str | None]:
    env_key = os.getenv("GEMINI_API_KEY") or os.getenv("API_GEMINI")
    if env_key:
        return env_key, "entorno del shell"

    parsed = parse_env_file(env_file)
    file_key = parsed.get("GEMINI_API_KEY") or parsed.get("API_GEMINI")
    if file_key:
        return file_key, str(env_file)

    return None, None


def get_client(env_file: Path) -> tuple[genai.Client | None, str | None]:
    api_key, source = get_gemini_api_key(env_file)
    if not api_key:
        return None, None

    return genai.Client(api_key=api_key), source


def discover_models_for_method(method: str, env_file: Path) -> list[str]:
    client, _ = get_client(env_file)
    if client is None:
        print("[WARN] No se encontro GEMINI_API_KEY/API_GEMINI para listar modelos.")
        return []

    try:
        models = list(client.models.list())
    except Exception as error:
        print(f"[WARN] No se pudieron listar modelos: {error}")
        return []

    discovered: list[str] = []
    for model in models:
        methods = getattr(model, "supported_generation_methods", None) or []
        if method in methods:
            name = getattr(model, "name", "")
            if name:
                discovered.append(name)

    return dedupe_models(discovered)


def extract_embedding(payload: object) -> list[float] | None:
    if isinstance(payload, dict):
        embedding = payload.get("embedding")
        if isinstance(embedding, list):
            return [float(value) for value in embedding]
        if isinstance(embedding, dict):
            values = embedding.get("values")
            if isinstance(values, list):
                return [float(value) for value in values]

    embedding_attr = getattr(payload, "embedding", None)
    if isinstance(embedding_attr, list):
        return [float(value) for value in embedding_attr]

    values_attr = getattr(embedding_attr, "values", None)
    if isinstance(values_attr, list):
        return [float(value) for value in values_attr]

    return None


def test_chat_model(model_name: str, env_file: Path) -> tuple[bool, str]:
    try:
        client, _ = get_client(env_file)
        if client is None:
            return False, "No se encontro GEMINI_API_KEY/API_GEMINI"

        response = client.models.generate_content(
            model=model_name,
            contents="Responde solo: OK",
            config=types.GenerateContentConfig(
                temperature=0.0,
                max_output_tokens=24,
            ),
        )
    except Exception as error:
        return False, str(error)

    text = (getattr(response, "text", "") or "").strip()
    if text:
        preview = text.replace("\n", " ")[:80]
        return True, f"OK -> {preview}"

    return False, "Respuesta vacia"


def test_embedding_model(model_name: str, env_file: Path) -> tuple[bool, str]:
    try:
        client, _ = get_client(env_file)
        if client is None:
            return False, "No se encontro GEMINI_API_KEY/API_GEMINI"

        response = client.models.embed_content(
            model=model_name,
            contents="consulta de prueba para embeddings",
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_QUERY",
                output_dimensionality=EMBEDDING_DIMENSIONALITY,
            ),
        )
    except Exception as error:
        return False, str(error)

    embedding = extract_embedding(response)
    if not embedding:
        return False, "Embedding vacio"

    return True, f"OK -> dimension {len(embedding)}"


def update_env_file(env_file: Path, chat_model: str | None, embedding_model: str | None) -> None:
    content = env_file.read_text(encoding="utf-8") if env_file.exists() else ""

    def upsert(key: str, value: str | None, text: str) -> str:
        if not value:
            return text

        pattern = re.compile(rf"^\s*{re.escape(key)}\s*=.*$", re.MULTILINE)
        replacement = f"{key}={value}"
        if pattern.search(text):
            return pattern.sub(replacement, text)

        if text and not text.endswith("\n"):
            text += "\n"
        return text + replacement + "\n"

    updated = content
    updated = upsert("GEMINI_CHAT_MODEL", chat_model, updated)
    updated = upsert("GEMINI_EMBEDDING_MODEL", embedding_model, updated)

    env_file.write_text(updated, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Probar acceso a modelos de Gemini.")
    parser.add_argument(
        "--update-env",
        action="store_true",
        help="Actualiza el archivo .env con los mejores modelos detectados.",
    )
    parser.add_argument(
        "--env-file",
        default="../.env",
        help="Ruta al archivo .env a actualizar (default: ../.env).",
    )
    args = parser.parse_args()

    env_path = resolve_env_path(args.env_file)

    api_key, source = get_gemini_api_key(env_path)
    if not api_key:
        print(
            "[ERROR] No se encontro GEMINI_API_KEY ni API_GEMINI "
            f"ni en el entorno ni en {env_path}."
        )
        return 2

    print(f"[INFO] Usando API key de Gemini desde: {source}")

    discovered_chat = discover_models_for_method("generateContent", env_path)
    discovered_embeddings = discover_models_for_method("embedContent", env_path)

    chat_models = dedupe_models(CHAT_CANDIDATES + discovered_chat)
    embedding_models = dedupe_models(EMBEDDING_CANDIDATES + discovered_embeddings)

    print("== Prueba de modelos de chat ==")
    best_chat_model: str | None = None
    for model_name in chat_models:
        ok, detail = test_chat_model(model_name, env_path)
        status = "OK" if ok else "FAIL"
        print(f"[{status}] {model_name}: {detail}")
        if ok and not best_chat_model:
            best_chat_model = model_name

    print("\n== Prueba de modelos de embeddings ==")
    best_embedding_model: str | None = None
    for model_name in embedding_models:
        ok, detail = test_embedding_model(model_name, env_path)
        status = "OK" if ok else "FAIL"
        print(f"[{status}] {model_name}: {detail}")
        if ok and not best_embedding_model:
            best_embedding_model = model_name

    print("\n== Recomendacion ==")
    if best_chat_model:
        print(f"GEMINI_CHAT_MODEL={best_chat_model}")
    else:
        print("GEMINI_CHAT_MODEL=<sin modelo accesible>")

    if best_embedding_model:
        print(f"GEMINI_EMBEDDING_MODEL={best_embedding_model}")
    else:
        print("GEMINI_EMBEDDING_MODEL=<sin modelo accesible>")

    if args.update_env:
        update_env_file(env_path, best_chat_model, best_embedding_model)
        print(f"\n[OK] Archivo actualizado: {env_path}")

    if not best_chat_model and not best_embedding_model:
        print("\n[WARN] No se detectaron modelos accesibles con esta API key.")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
