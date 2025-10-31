# DESCRIPTIONS: Tiny agent that reads env vars; loads .env when running locally; posts to OpenAI-compatible Chat API.

# DESCRIPTIONS: Imports and optional .env loader (no-op in Docker if you pass envs at runtime)
import os, requests, sys
try:
    # DESCRIPTIONS: Load .env from current directory (override=False keeps real env winning in Docker)
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=os.getenv("ENV_FILE", ".env"), override=False)
except Exception:
    pass  # DESCRIPTIONS: Safe if python-dotenv isn't installed

# DESCRIPTIONS: Config from environment with sensible defaults
API_BASE = os.getenv("API_BASE", "https://api.openai.com/v1")
API_KEY  = os.getenv("API_KEY") or os.getenv("OPENAI_API_KEY")
MODEL    = os.getenv("MODEL", "gpt-4o-mini")
TASK     = os.getenv("TASK", "Say hello briefly.")

# DESCRIPTIONS: Fail fast if we need a key (Ollama can be keyless; OpenAI needs one)
if "openai.com" in API_BASE and not API_KEY:
    print("[agent error] Missing API_KEY/OPENAI_API_KEY for OpenAI endpoint.", file=sys.stderr)
    sys.exit(1)

# DESCRIPTIONS: HTTP request to Chat Completions; prints assistant reply or readable error
headers = {"Content-Type": "application/json"}
if API_KEY:
    headers["Authorization"] = f"Bearer {API_KEY}"
payload = {
    "model": MODEL,
    "messages": [
        {"role": "system", "content": "You are a helpful general-purpose agent."},
        {"role": "user",   "content": TASK}
    ]
}

try:
    r = requests.post(f"{API_BASE}/chat/completions", headers=headers, json=payload, timeout=60)
    r.raise_for_status()
    print(r.json()["choices"][0]["message"]["content"])
except Exception as e:
    err = getattr(getattr(e, "response", None), "text", None) or str(e)
    print(f"[agent error] {err}", file=sys.stderr)
    sys.exit(1)
