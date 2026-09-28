"""Quick benchmark for Fast-agent (direct LLM, no tools) response time across models.

Usage:
    python3 benchmark_fast.py --models mistralai/Mistral-7B-Instruct-v0.3 meta-llama/Meta-Llama-3.1-8B-Instruct zai-org/GLM-4.5-Air --response-type Short
"""
import argparse
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from prompts import quick_response_system_prompt

load_dotenv(dotenv_path=Path('/home/gz/Documents/Rebuttal AI/.env'))
API_TOKEN = os.environ['API_TOKEN']
BASE_URL = "https://api.deepinfra.com/v1/openai"

DEFAULT_CLAIM = "Tariffs on imported goods always protect local jobs and boost domestic businesses."


def time_one_model(model: str, response_type: str, style: str = "Academic", claim: str = DEFAULT_CLAIM, max_tokens: int = 800):
    """Run one Fast-style invoke and return (seconds, chars, ok, preview_or_error)."""
    llm = ChatOpenAI(api_key=API_TOKEN, model=model, base_url=BASE_URL, max_tokens=max_tokens, timeout=60)
    agent_prompt = f"claim:{claim} \n style:{style}\n length:{response_type}"
    messages = [("system", quick_response_system_prompt), ("human", agent_prompt)]
    t0 = time.time()
    try:
        result = llm.invoke(messages)
        dt = time.time() - t0
        content = result.content or ""
        return dt, len(content), True, content[:80].replace("\n", " ")
    except Exception as e:
        return time.time() - t0, 0, False, str(e)[:80]


def benchmark_fast(models, response_type: str = "Short", style: str = "Academic"):
    """Time each model and print a console table. Returns list of dicts."""
    if len(models) != 3:
        print(f"Note: expected 3 models, got {len(models)} — running anyway.")
    results = []
    for model in models:
        dt, n_chars, ok, preview = time_one_model(model, response_type, style)
        results.append({"model": model, "time_s": dt, "chars": n_chars, "ok": ok, "preview": preview})

    # Console table (no extra deps)
    print(f"\nFast response benchmark | type={response_type} style={style}")
    print("-" * 90)
    print(f"{'Model':<45} {'Time (s)':>9} {'Chars':>7}  Status")
    print("-" * 90)
    for r in results:
        status = "OK" if r["ok"] else f"FAIL: {r['preview']}"
        extra = f" | {r['preview']}..." if r["ok"] else ""
        print(f"{r['model']:<45} {r['time_s']:>9.2f} {r['chars']:>7}  {status}{extra}")
    print("-" * 90)
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Benchmark Fast-agent response time for 3 models.")
    parser.add_argument("--models", nargs=3, required=False,
                        default=["meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
                                 "openai/gpt-oss-120b-Turbo",
                                 "openai/gpt-oss-120b"],
                        help="Exactly three DeepInfra model ids.")
    parser.add_argument("--response-type", default="Short", choices=["Short", "Medium", "Long"],
                        help="Length type passed to the fast prompt.")
    parser.add_argument("--style", default="Academic")
    args = parser.parse_args()
    benchmark_fast(list(args.models), response_type=args.response_type, style=args.style)
