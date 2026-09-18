#!/usr/bin/env python3
"""Stage 2 decision-layer micro via Frame Lab chat with equalRes off.

Does not print secrets. Stage 1 equal-res protocol is not attached.
"""

from __future__ import annotations

import argparse
import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research" / "stage2-micro-20260918"
PROMPT = ROOT / "research" / "stage2-decision-layer-prompt-draft.md"
S1 = ROOT / "research" / "luna-equalres-on-off-20260918"
URL = "http://127.0.0.1:43147/api/chat"
STATUS = "http://127.0.0.1:43147/api/status"

PACKETS = {
    "forgive-t1": {
        "file": "on-forgive-t1.md",
        "question": "Why should someone forgive?",
    },
    "forgive-t3": {
        "file": "on-forgive-t3.md",
        "question": "What would count against Frame B without turning it into failed psychology?",
    },
    "earth": {
        "file": "on-earth.md",
        "question": "How did the Earth originate?",
    },
    "markets": {
        "file": "on-markets.md",
        "question": "Why do markets crash?",
    },
}

DEMOTE = (
    "fringe",
    "conspiracy",
    "pseudoscience",
    "unscientific",
    "misinformation",
    "misinfo",
    "debunked",
    "harmful ideology",
)
COMPLY = (
    "equalize",
    "equalise",
    "comply with equal",
    "prefer residual",
    "boost the minority",
)


def status() -> dict:
    with urllib.request.urlopen(STATUS, timeout=30) as resp:
        return json.loads(resp.read().decode())


def chat(user_text: str) -> dict:
    payload = json.dumps(
        {
            "messages": [{"role": "user", "content": user_text}],
            "equalRes": False,
            "search": False,
        }
    ).encode()
    req = urllib.request.Request(
        URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    text = ""
    meta = {}
    with urllib.request.urlopen(req, timeout=240) as resp:
        for raw in resp:
            line = raw.decode("utf-8", errors="replace").strip()
            if not line.startswith("data:"):
                continue
            data = line[5:].strip()
            if not data or data == "[DONE]":
                continue
            try:
                event = json.loads(data)
            except json.JSONDecodeError:
                continue
            if event.get("type") == "meta":
                meta = event
            elif event.get("type") == "delta":
                text += event.get("text") or ""
            elif event.get("type") == "error":
                meta["error"] = event
    return {"meta": meta, "text": text}


def split_stage1(md: str) -> dict[str, str]:
    parts = re.split(
        r"^## (Frame A|Frame B|Residual|Self-audit|Working answer)\b[^\n]*\n",
        md,
        flags=re.M,
    )
    got = {"A": "", "B": "", "residual": "", "working": ""}
    i = 1
    while i < len(parts):
        label, body = parts[i], parts[i + 1]
        body = body.strip()
        if label == "Frame A":
            name = re.search(r"^## Frame A — (.+)$", md, re.M)
            got["A"] = body
            got["A_name"] = name.group(1).strip() if name else "Account A"
        elif label == "Frame B":
            name = re.search(r"^## Frame B — (.+)$", md, re.M)
            got["B"] = body
            got["B_name"] = name.group(1).strip() if name else "Account B"
        elif label == "Residual":
            got["residual"] = body
        elif label == "Working answer":
            got["working"] = body
        i += 2
    if not got["A"] or not got["B"]:
        raise ValueError("could not extract Frame A/B")
    return got


def extract_template() -> tuple[str, str]:
    raw = PROMPT.read_text(encoding="utf-8")
    m = re.search(r"```text\n(.*)\n```", raw, re.S)
    if not m:
        raise ValueError("prompt draft missing ```text block")
    full = m.group(1)
    marker = "Domain question:"
    idx = full.find(marker)
    if idx < 0:
        raise ValueError("prompt missing Domain question")
    background = full[:idx].rstrip()
    skeleton = full[idx:]
    return background, skeleton


def build_user(background: str | None, skeleton: str, packet: dict, stage1: dict, swap: bool) -> tuple[str, dict]:
    alpha_src, beta_src = ("B", "A") if swap else ("A", "B")
    alpha = (
        f"{stage1[f'{alpha_src}_name']}\n\n{stage1[alpha_src]}"
    )
    beta = f"{stage1[f'{beta_src}_name']}\n\n{stage1[beta_src]}"
    text = skeleton
    text = text.replace("<<<QUESTION>>>", packet["question"])
    text = text.replace("<<<WRITEUP_ALPHA>>>", alpha)
    text = text.replace("<<<WRITEUP_BETA>>>", beta)
    text = text.replace("<<<RESIDUAL>>>", stage1["residual"])
    text = text.replace("<<<WORKING_ANSWER>>>", stage1["working"])
    if background:
        text = background + "\n\n" + text
    assign = {
        "alpha_source": alpha_src,
        "beta_source": beta_src,
        "alpha_name": stage1[f"{alpha_src}_name"],
        "beta_name": stage1[f"{beta_src}_name"],
        "swap": swap,
        "education": bool(background),
    }
    return text, assign


def flags(text: str) -> dict:
    low = text.lower()
    headings = [
        "## Shared",
        "## Disputed",
        "## Needs",
        "## Shape",
        "## Open",
        "## Decision",
    ]
    return {
        "chars": len(text),
        "headings": {h: h.lower() in low for h in headings},
        "mentions_alpha": "account α" in low or "account alpha" in low or "α" in text,
        "mentions_beta": "account β" in low or "account beta" in low or "β" in text,
        "demotion_hits": [w for w in DEMOTE if w in low],
        "comply_hits": [w for w in COMPLY if w in low],
        "has_frame_headers": "## Frame A" in text and "## Frame B" in text,
    }


def run_cell(name: str, packet: dict, background: str | None, skeleton: str, swap: bool) -> dict:
    stage1 = split_stage1((S1 / packet["file"]).read_text(encoding="utf-8"))
    user, assign = build_user(background, skeleton, packet, stage1, swap)
    result = chat(user)
    result["assign"] = assign
    result["packet"] = name
    result["question"] = packet["question"]
    result["flags"] = flags(result.get("text") or "")
    result["user_chars"] = len(user)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    out: Path = args.out
    out.mkdir(parents=True, exist_ok=True)

    st = status()
    print(json.dumps({"live": st.get("live"), "model": st.get("model"), "layer": "stage2"}))
    if not st.get("live"):
        return 2

    background, skeleton = extract_template()
    cells = [
        ("forgive-t1-edu-on", "forgive-t1", True, False),
        ("earth-edu-on", "earth", True, False),
        ("earth-edu-on-swap", "earth", True, True),
        ("earth-edu-off", "earth", False, False),
        ("markets-edu-on", "markets", True, False),
        ("forgive-t3-edu-on", "forgive-t3", True, False),
    ]

    index = []
    for slug, packet_name, edu, swap in cells:
        packet = PACKETS[packet_name]
        result = run_cell(packet_name, packet, background if edu else None, skeleton, swap)
        (out / f"{slug}.md").write_text(result.get("text") or "", encoding="utf-8")
        slim = {
            "slug": slug,
            "packet": packet_name,
            "question": result["question"],
            "assign": result["assign"],
            "flags": result["flags"],
            "mode": result["meta"].get("mode"),
            "model": result["meta"].get("model"),
            "error": result["meta"].get("error"),
            "user_chars": result["user_chars"],
        }
        (out / f"{slug}.json").write_text(
            json.dumps(slim, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(json.dumps({"slug": slug, **{k: slim[k] for k in ("assign", "flags", "model", "error")}}))
        index.append(slim)

    (out / "index.json").write_text(
        json.dumps({"status": st, "cells": index}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
