# DESCRIPTIONS: Tiny AI agent that reads a TASK from environment, calls an OpenAI-compatible Chat Completions API, and prints the reply.

# DESCRIPTIONS: Imports (os for env, requests for HTTP, sys for clean error output)
import os, requests, sys

# DESCRIPTIONS: Config from environment with safe defaults (works with OpenAI, OpenRouter, or local Ollama if API_BASE points there)
API_BASE = os.getenv("API_BASE", "https://api.openai.com/v1")
API_KEY  = os.getenv("API_KEY") or os.getenv("OPENAI_API_KEY")
MODEL    = os.getenv("MODEL", "gpt-4o-mini")
TASK     = os.getenv("TASK", "Say hello briefly.")

# DESCRIPTIONS: HTTP headers (Authorization only if a key is supplied) and minimal Chat Completions payload
headers = {"Content-Type": "application/json"}
if API_KEY:
    headers["Authorization"] = f"Bearer {API_KEY}"
body = {
    "model": MODEL,
    "messages": [
        {"role": "system", "content": "You are a helpful general-purpose agent."},
        {"role": "user",   "content": TASK}
    ]
}

# DESCRIPTIONS: Send request, print assistant message on success, show readable error on failure
try:
    resp = requests.post(f"{API_BASE}/chat/completions", headers=headers, json=body, timeout=60)
    resp.raise_for_status()
    print(resp.json()["choices"][0]["message"]["content"])
except Exception as e:
    err_text = getattr(getattr(e, "response", None), "text", None) or str(e)
    print(f"[agent error] {err_text}", file=sys.stderr)
    sys.exit(1)
