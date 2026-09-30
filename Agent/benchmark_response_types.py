"""Benchmark Research vs Web Agent vs Fast on a SINGLE model.

Standalone script — does not modify any existing workflow files.
Mirrors Agent/LLM_Agents.py agent construction inline so LLM_Agents.py
stays untouched, and mirrors benchmark_fast.py console-table style.

Usage (run from the Agent/ directory):
    python3 benchmark_response_types.py --model openai/gpt-oss-120b-Turbo --runs 3
    python3 benchmark_response_types.py --model openai/gpt-oss-120b-Turbo --runs 3 --output results.json
    python3 benchmark_response_types.py --types fast web --runs 2 --length Short --style Academic
"""

import argparse
import csv
import json
import os
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

# Imports mirror LLM_Agents.py / benchmark_fast.py (read-only, no edits there).
from langchain.agents import create_agent
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI

from LLM_Tools import logical_fallacies_retriever, search, wiki_summary
from prompts import (
    quick_response_system_prompt,
    research_system_prompt,
    web_search_agent_prompt,
)

load_dotenv(dotenv_path=Path('/home/gz/Documents/Rebuttal AI/.env'))
API_TOKEN = os.environ['API_TOKEN']
BASE_URL = "https://api.deepinfra.com/v1/openai"

DEFAULT_CLAIM = "Tariffs on imported goods always protect local jobs and boost domestic businesses."
AGENT_TYPES = ("fast", "web", "research")


def build_agents(model: str, recursion_limit: int):
    """Build llm + agents inline (same construction as LLM_Agents.Agent)."""
    llm = ChatOpenAI(
        api_key=API_TOKEN,
        model=model,
        base_url=BASE_URL,
        max_tokens=1500,
        timeout=30,
    )
    research_agent = create_agent(
        model=llm,
        tools=[search, logical_fallacies_retriever, wiki_summary],
        system_prompt=research_system_prompt,
    )
    web_agent = create_agent(
        model=llm,
        tools=[search],
        system_prompt=web_search_agent_prompt,
    )
    return llm, research_agent, web_agent


def warmup_vector_db() -> tuple[float, bool, str]:
    """Preload the FAISS fallacy DB (local only, no LLM call) so the first
    timed Research run isn't skewed by cold-start embedding/DB load."""
    t0 = time.perf_counter()
    try:
        from LLM_Tools import _get_db_retriever

        _get_db_retriever()
        return time.perf_counter() - t0, True, "vector DB preloaded"
    except Exception as e:  # noqa: BLE001 — report, don't crash benchmark
        return time.perf_counter() - t0, False, str(e)[:120]


def run_once(agent_type: str, llm, research_agent, web_agent,
             claim: str, recursion_limit: int, parser: JsonOutputParser):
    """Run one response and return (seconds, chars, ok, preview_or_error)."""
    agent_prompt = f"claim:{claim} \n style:{STYLE}\n length:{LENGTH}"
    t0 = time.perf_counter()
    try:
        if agent_type == "fast":
            messages = [("system", quick_response_system_prompt), ("human", agent_prompt)]
            result = llm.invoke(messages)
            parsed = parser.parse(result.content)
        elif agent_type == "web":
            result = web_agent.invoke(
                {"messages": [{"role": "user", "content": agent_prompt}]},
                config={"recursion_limit": recursion_limit},
            )
            parsed = parser.parse(result["messages"][-1].content)
        else:  # research
            result = research_agent.invoke(
                {"messages": [{"role": "user", "content": agent_prompt}]},
                config={"recursion_limit": recursion_limit},
            )
            parsed = parser.parse(result["messages"][-1].content)
        dt = time.perf_counter() - t0
        content = parsed.get("response", "") if isinstance(parsed, dict) else str(parsed)
        details = parsed.get("details", "") if isinstance(parsed, dict) else ""
        n_chars = len(str(content)) + len(str(details))
        preview = str(content)[:80].replace("\n", " ")
        return dt, n_chars, True, preview
    except Exception as e:  # noqa: BLE001 — a failed run is a data point
        return time.perf_counter() - t0, 0, False, str(e)[:120]


def print_run_table(rows):
    print(f"\nPer-run results | model={MODEL} length={LENGTH} style={STYLE}")
    print("-" * 100)
    print(f"{'Type':<9} {'Run':>3} {'Time (s)':>9} {'Chars':>7}  Status")
    print("-" * 100)
    for r in rows:
        status = "OK" if r["ok"] else f"FAIL: {r['preview']}"
        extra = f" | {r['preview']}..." if r["ok"] else ""
        print(f"{r['type']:<9} {r['run']:>3} {r['time_s']:>9.2f} {r['chars']:>7}  {status}{extra}")
    print("-" * 100)


def print_summary_table(summary, fast_mean: float | None):
    print(f"\nSummary (mean over successful runs) | model={MODEL}")
    print("-" * 100)
    print(f"{'Type':<9} {'n_ok/n':>7} {'Mean (s)':>9} {'Min (s)':>8} {'Max (s)':>8} {'Avg chars':>9}  vs Fast")
    print("-" * 100)
    for agent_type in AGENT_TYPES:
        s = summary.get(agent_type)
        if not s or not s.get("n_ok"):
            print(f"{agent_type:<9} {'0/0':>7} {'—':>9} {'—':>8} {'—':>8} {'—':>9}")
            continue
        ratio = ""
        if fast_mean and agent_type != "fast":
            ratio = f"{s['mean'] / fast_mean:.1f}x slower"
        elif agent_type == "fast":
            ratio = "baseline"
        print(
            f"{agent_type:<9} {s['n_ok']:>3}/{s['n']:>3}"
            f" {s['mean']:>9.2f} {s['min']:>8.2f} {s['max']:>8.2f} {s['avg_chars']:>9.0f}  {ratio}"
        )
    print("-" * 100)


def save_results(path: Path, payload: dict):
    path.write_text(json.dumps(payload, indent=2))
    csv_path = path.with_suffix(".csv")
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["type", "run", "time_s", "chars", "ok", "preview"])
        writer.writeheader()
        writer.writerows(payload["runs"])
    print(f"Saved JSON → {path}")
    print(f"Saved CSV  → {csv_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Time Research vs Web vs Fast response types on one model."
    )
    parser.add_argument("--model", default="openai/gpt-oss-120b-Turbo",
                        help="Single DeepInfra model id used for all three types.")
    parser.add_argument("--types", nargs="+", default=list(AGENT_TYPES),
                        choices=list(AGENT_TYPES),
                        help="Subset/order of response types to benchmark.")
    parser.add_argument("--runs", type=int, default=3,
                        help="Timed runs per response type (averaged).")
    parser.add_argument("--length", default="Short", choices=["Short", "Medium", "Long"],
                        help="Length passed to the agent prompt.")
    parser.add_argument("--style", default="Academic")
    parser.add_argument("--claim", default=DEFAULT_CLAIM)
    parser.add_argument("--recursion-limit", type=int,
                        default=int(os.environ.get("AGENT_RECURSION_LIMIT", "6")))
    parser.add_argument("--sleep", type=float, default=2.0,
                        help="Seconds to sleep between runs (e.g. DuckDuckGo rate limits).")
    parser.add_argument("--no-warmup", action="store_true",
                        help="Skip vector-DB preload; first Research run includes cold start.")
    parser.add_argument("--output", default=None,
                        help="Path to save JSON results (CSV saved alongside).")
    args = parser.parse_args()

    # Module-level for run_once() + table printers (keeps signatures short).
    MODEL = args.model
    LENGTH = args.length
    STYLE = args.style

    if args.runs < 1:
        sys.exit("--runs must be >= 1")

    llm, research_agent, web_agent = build_agents(args.model, args.recursion_limit)
    json_parser = JsonOutputParser()

    if not args.no_warmup:
        w_dt, w_ok, w_msg = warmup_vector_db()
        print(f"Warmup: vector DB preload took {w_dt:.2f}s — {'OK' if w_ok else 'SKIPPED'} ({w_msg})")
    else:
        print("Warmup skipped (--no-warmup): first Research run includes cold start.")

    rows: list[dict] = []
    for agent_type in args.types:
        for i in range(1, args.runs + 1):
            print(f"Running {agent_type} ({i}/{args.runs})...", flush=True)
            dt, n_chars, ok, preview = run_once(
                agent_type, llm, research_agent, web_agent,
                args.claim, args.recursion_limit, json_parser,
            )
            rows.append({"type": agent_type, "run": i, "time_s": round(dt, 2),
                         "chars": n_chars, "ok": ok, "preview": preview})
            if args.sleep and not (agent_type == args.types[-1] and i == args.runs):
                time.sleep(args.sleep)

    print_run_table(rows)

    summary: dict = {}
    for agent_type in args.types:
        ok_times = [r["time_s"] for r in rows if r["type"] == agent_type and r["ok"]]
        ok_chars = [r["chars"] for r in rows if r["type"] == agent_type and r["ok"]]
        n = sum(1 for r in rows if r["type"] == agent_type)
        summary[agent_type] = {
            "n": n,
            "n_ok": len(ok_times),
            "mean": round(statistics.mean(ok_times), 2) if ok_times else None,
            "min": round(min(ok_times), 2) if ok_times else None,
            "max": round(max(ok_times), 2) if ok_times else None,
            "avg_chars": round(statistics.mean(ok_chars), 1) if ok_chars else None,
        }
    fast_mean = summary.get("fast", {}).get("mean")
    print_summary_table(summary, fast_mean)

    if args.output:
        payload = {
            "model": args.model,
            "length": args.length,
            "style": args.style,
            "claim": args.claim,
            "runs_per_type": args.runs,
            "recursion_limit": args.recursion_limit,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "summary": summary,
            "runs": rows,
        }
        save_results(Path(args.output), payload)
