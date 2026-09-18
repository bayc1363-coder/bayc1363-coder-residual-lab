#!/usr/bin/env python3
"""Live OFF/ON relative-decision probe with locked concept vocab.

claim_level=synthetic. Length never a win condition.
Win OFF→ON = lower |soft_rank_skew|.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from residual_lab.relative_decision import compare_off_on, load_prereg, run_topic

PREREG = ROOT / "batteries" / "concept_vocab_prereg_v2.yaml"
RD_ON_CUE = (ROOT / "filters" / "relative_decision" / "rd_on_cue_v1.txt").read_text(encoding="utf-8")


def load_key() -> str:
    key = os.environ.get("EXPLABS_API_KEY") or os.environ.get("EXPERIENTIAL_API_KEY")
    if key:
        return key
    for p in (
        Path("/home/box/sand-data/box-secrets.json"),
        Path("/home/box/agent-data/box-secrets.json"),
    ):
        if p.exists():
            j = json.loads(p.read_text())
            card = j.get("card") or j
            for k in ("EXPLABS_API_KEY", "EXPERIENTIAL_API_KEY"):
                if card.get(k):
                    return card[k]
    raise SystemExit("no EXPLABS_API_KEY")



def experiential_complete(model: str, system: str | None, user: str, max_tokens: int = 400) -> str:
    key = load_key()
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": user})
    body = json.dumps(
        {
            "model": model,
            "messages": messages,
            "temperature": 0.2,
            "max_tokens": max_tokens,
        }
    ).encode()
    req = urllib.request.Request(
        "https://api.experientiallabs.ai/v1/chat/completions",
        data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                j = json.loads(r.read().decode())
            msg = (j.get("choices") or [{}])[0].get("message") or {}
            content = (msg.get("content") or "").strip()
            if content:
                return content
            time.sleep(1.5 * (attempt + 1))
        except Exception as e:
            if attempt == 2:
                return f"ERROR: {type(e).__name__}: {e}"
            time.sleep(2 * (attempt + 1))
    return "ERROR: empty"


def ollama_complete(model: str, system: str | None, user: str, base: str = "http://127.0.0.1:11434") -> str:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": user})
    body = json.dumps(
        {
            "model": model,
            "messages": messages,
            "stream": False,
            "think": False,
            "keep_alive": "20m",
            "options": {"temperature": 0.2, "num_predict": 400},
        }
    ).encode()
    req = urllib.request.Request(
        base + "/api/chat",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=600) as r:
        j = json.loads(r.read().decode())
    msg = j.get("message") or {}
    return (msg.get("content") or msg.get("thinking") or "").strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--backend", choices=["experiential", "ollama"], required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--topics", default="earth,dna,constants,forgiveness")
    ap.add_argument("--seed", type=int, default=17)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()
    out = args.out or (ROOT / "out" / "p0-runs" / f"relative-decision-live-{args.backend}-{args.model.replace(':','_')}")
    out.mkdir(parents=True, exist_ok=True)
    prereg = load_prereg(PREREG)
    topics = [t.strip() for t in args.topics.split(",") if t.strip()]

    def make_complete(filter_on: bool):
        # v2: thin RD equal-prior cue only — NOT equal-res essay filter
        system = RD_ON_CUE if filter_on else None

        def complete(prompt: str) -> str:
            if args.backend == "experiential":
                return experiential_complete(args.model, system, prompt)
            return ollama_complete(args.model, system, prompt)

        return complete

    lines = [
        f"# Relative-decision LIVE — {args.backend} / `{args.model}`",
        "",
        "claim_level: **synthetic**. Length ignored. Win = lower |soft_rank_skew| ON vs OFF.",
        f"vocab: `{PREREG.name}` locked (de-tainted v2).",
        "ON cue: `rd_on_cue_v1.txt` (thin equal-prior — not equal-res essay).",
        "",
        "| topic | off_skew | on_skew | off_canon | on_canon | pass | notes |",
        "| --- | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for topic in topics:
        print(f"=== {args.model} {topic} OFF ===", flush=True)
        off = run_topic(
            prereg=prereg,
            topic=topic,
            complete=make_complete(False),
            seed=args.seed,
            filter_on=False,
        )
        print(f"=== {args.model} {topic} ON ===", flush=True)
        on = run_topic(
            prereg=prereg,
            topic=topic,
            complete=make_complete(True),
            seed=args.seed + 1,
            filter_on=True,
        )
        cmp_ = compare_off_on(off["scores"], on["scores"])
        (out / f"{topic}__off.json").write_text(json.dumps(off, indent=2), encoding="utf-8")
        (out / f"{topic}__on.json").write_text(json.dumps(on, indent=2), encoding="utf-8")
        (out / f"{topic}__compare.json").write_text(json.dumps(cmp_, indent=2), encoding="utf-8")
        lines.append(
            f"| {topic} | {off['scores']['soft_rank_skew']} | {on['scores']['soft_rank_skew']} | "
            f"{off['scores']['canonical_pick_rate']} | {on['scores']['canonical_pick_rate']} | "
            f"{'PASS' if cmp_['pass'] else 'FAIL'} | {'; '.join(cmp_['notes'])} |"
        )
        print(json.dumps({"topic": topic, **cmp_}), flush=True)

    report = "\n".join(lines) + "\n"
    (out / "REPORT.md").write_text(report, encoding="utf-8")
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
