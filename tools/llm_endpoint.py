"""Resolve a self-hosted or OpenAI endpoint without embedding tunnel URLs or leaking keys."""
import os
from urllib.parse import urlparse

OPENAI_API_HOST = "api.openai.com"


class LlmEndpointError(ValueError):
    """The caller did not provide an endpoint or a key that is safe to send there."""


def normalize_base_url(url):
    raw = url.strip().rstrip("/")
    if raw.endswith("/chat/completions"):
        raw = raw[: -len("/chat/completions")].rstrip("/")
    if not raw.endswith("/v1"):
        raw = raw + "/v1"
    return raw


def resolve_base_url(explicit=None, provider=None):
    """Return an OpenAI-compatible /v1 base URL.

    Self-hosted endpoints have no built-in default. Only the OpenAI provider
    may fall back to api.openai.com.
    """
    raw = (explicit or os.getenv("NEBULITH_LLM_ENDPOINT") or os.getenv("COLAB_LLM_ENDPOINT") or "").strip()
    if not raw and provider == "openai":
        raw = (os.getenv("OPENAI_BASE_URL") or "https://api.openai.com/v1").strip()
    if not raw:
        raise LlmEndpointError(
            "LLMの接続先が未指定です。--endpoint か環境変数 NEBULITH_LLM_ENDPOINT を指定してください。"
            "公開トンネルのURLは既定値にしません。"
        )
    return normalize_base_url(raw)


def resolve_api_key(base_url, explicit=None):
    """OPENAI_API_KEY is sent only to api.openai.com. Other hosts use NEBULITH_LLM_API_KEY."""
    if explicit:
        return explicit
    host = (urlparse(base_url).hostname or "").lower()
    if host == OPENAI_API_HOST:
        return os.getenv("OPENAI_API_KEY", "")
    return os.getenv("NEBULITH_LLM_API_KEY", "")


def missing_key_message(base_url):
    host = (urlparse(base_url).hostname or "").lower()
    if host == OPENAI_API_HOST:
        return "api.openai.com には OPENAI_API_KEY か --api-key が必要です。"
    return (
        "この接続先には NEBULITH_LLM_API_KEY か --api-key が必要です。"
        "OPENAI_API_KEY は api.openai.com 以外へは送りません。"
    )


def authorization_headers(base_url, explicit=None):
    key = resolve_api_key(base_url, explicit)
    if not key:
        raise LlmEndpointError(missing_key_message(base_url))
    return {"Authorization": "Bearer " + key}
