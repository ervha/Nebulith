import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from llm_endpoint import LlmEndpointError, authorization_headers, resolve_api_key, resolve_base_url


class LlmEndpointTests(unittest.TestCase):
    def setUp(self):
        self._env = {name: os.environ.get(name) for name in ("OPENAI_API_KEY", "NEBULITH_LLM_API_KEY", "NEBULITH_LLM_ENDPOINT", "COLAB_LLM_ENDPOINT", "OPENAI_BASE_URL")}
        for name in self._env:
            os.environ.pop(name, None)

    def tearDown(self):
        for name, value in self._env.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value

    def test_openai_key_stays_on_openai_host(self):
        os.environ["OPENAI_API_KEY"] = "sk-real"
        os.environ["NEBULITH_LLM_API_KEY"] = "self-hosted"
        self.assertEqual("sk-real", resolve_api_key("https://api.openai.com/v1"))
        tunnel = "https://medieval-chance-starter-happen.trycloudflare.com/v1"
        self.assertEqual("self-hosted", resolve_api_key(tunnel))
        self.assertEqual("Bearer self-hosted", authorization_headers(tunnel)["Authorization"])
        self.assertNotIn("sk-real", authorization_headers(tunnel)["Authorization"])

    def test_self_hosted_endpoint_is_required(self):
        with self.assertRaises(LlmEndpointError):
            resolve_base_url(None, provider="colab")
        self.assertEqual("https://api.openai.com/v1", resolve_base_url(None, provider="openai"))
        os.environ["NEBULITH_LLM_ENDPOINT"] = "https://example.test/v1/"
        self.assertEqual("https://example.test/v1", resolve_base_url(None, provider="colab"))

    def test_sources_have_no_hardcoded_tunnel(self):
        banned = "medieval-chance-starter-happen.trycloudflare.com"
        paths = [
            ROOT / "tools/llm_agent_dialogue.py",
            ROOT / "tools/batch_colab_lexicon_expansion.py",
            ROOT / "tools/batch_colab_daily_conversation_expansion.py",
            ROOT / "colab/README.md",
            ROOT / "colab/nebulith_inference_server.ipynb",
        ]
        for path in paths:
            self.assertNotIn(banned, path.read_text(encoding="utf-8"), path.name)
        notebook = (ROOT / "colab/nebulith_inference_server.ipynb").read_text(encoding="utf-8")
        self.assertIn("--api-key", notebook)
        self.assertIn("NEBULITH_LLM_API_KEY", notebook)

    def test_dialogue_cli_refuses_missing_endpoint(self):
        env = os.environ.copy()
        for name in ("OPENAI_API_KEY", "NEBULITH_LLM_API_KEY", "NEBULITH_LLM_ENDPOINT", "COLAB_LLM_ENDPOINT", "OPENAI_BASE_URL"):
            env.pop(name, None)
        result = subprocess.run(
            [sys.executable, "tools/llm_agent_dialogue.py", "--health-check"],
            cwd=ROOT, capture_output=True, text=True, env=env, timeout=20,
        )
        self.assertNotEqual(0, result.returncode)
        self.assertNotIn("sk-", result.stdout + result.stderr)
        self.assertIn("NEBULITH_LLM_ENDPOINT", result.stderr + result.stdout)


if __name__ == "__main__":
    unittest.main()
