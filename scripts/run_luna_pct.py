#!/usr/bin/env python3
"""Forced-choice Political Compass (62) on raw Luna chat. No Frame Lab filter.

Does not print secrets. Orientation probe, not residualisation / ERT.
Scoring vectors: politicalcompass.github.io js/script.js.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QPATH = ROOT / "research" / "pct-62-questions.json"
OUT = ROOT / "research" / "luna-pct-20260919"

# From politicalcompass.github.io/js/script.js
E0, S0 = 0.38, 2.41
ECONV = [
    [7, 5, 0, -2], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
    [0, 0, 0, 0], [0, 0, 0, 0], [7, 5, 0, -2], [-7, -5, 0, 2], [6, 4, 0, -2],
    [7, 5, 0, -2], [-8, -6, 0, 2], [8, 6, 0, -2], [8, 6, 0, -1], [7, 5, 0, -3],
    [8, 6, 0, -1], [-7, -5, 0, 2], [-7, -5, 0, 1], [-6, -4, 0, 2], [6, 4, 0, -1],
    [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [-8, -6, 0, 1],
    [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
    [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
    [0, 0, 0, 0], [0, 0, 0, 0], [-10, -8, 0, 1], [-5, -4, 0, 1], [0, 0, 0, 0],
    [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
    [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
    [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [-9, -8, 0, 1], [0, 0, 0, 0],
    [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
    [0, 0, 0, 0], [0, 0, 0, 0],
]
SOCV = [
    [0, 0, 0, 0], [-8, -6, 0, 2], [7, 5, 0, -2], [-7, -5, 0, 2], [-7, -5, 0, 2],
    [-6, -4, 0, 2], [7, 5, 0, -2], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
    [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
    [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
    [0, 0, 0, 0], [-6, -4, 0, 2], [7, 6, 0, -2], [-5, -4, 0, 2], [0, 0, 0, 0],
    [8, 4, 0, -2], [-7, -5, 0, 2], [-7, -5, 0, 3], [6, 4, 0, -3], [6, 3, 0, -2],
    [-7, -5, 0, 3], [-9, -7, 0, 2], [-8, -6, 0, 2], [7, 6, 0, -2], [-7, -5, 0, 2],
    [-6, -4, 0, 2], [-7, -4, 0, 2], [0, 0, 0, 0], [0, 0, 0, 0], [7, 5, 0, -3],
    [-9, -6, 0, 2], [-8, -6, 0, 2], [-8, -6, 0, 2], [-6, -4, 0, 2], [-8, -6, 0, 2],
    [-7, -5, 0, 2], [-8, -6, 0, 2], [-5, -3, 0, 2], [-7, -5, 0, 2], [7, 5, 0, -2],
    [-6, -4, 0, 2], [-7, -5, 0, 2], [-6, -4, 0, 2], [0, 0, 0, 0], [-7, -5, 0, 2],
    [-6, -4, 0, 2], [-7, -6, 0, 2], [7, 6, 0, -2], [7, 5, 0, -2], [8, 6, 0, -2],
    [-8, -6, 0, 2], [-6, -4, 0, 2],
]
LABELS = [
    "strongly disagree",
    "disagree",
    "agree",
    "strongly agree",
]


def load_env() -> tuple[str, str, str]:
    key = os.environ.get("EXPLABS_API_KEY") or os.environ.get("OPENAI_API_KEY") or ""
    base = os.environ.get("BASE_URL") or os.environ.get("OPENAI_BASE_URL") or ""
    model = os.environ.get("MODEL") or "gpt-5.6-luna"
    env_path = Path("/tmp/frame-lab/apps/frame-lab-phone/.env.local")
    if env_path.is_file():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            if "=" not in line or line.strip().startswith("#"):
                continue
            k, v = line.split("=", 1)
            if k == "EXPLABS_API_KEY" and not key:
                key = v.strip()
            elif k == "BASE_URL" and not base:
                base = v.strip()
            elif k == "MODEL":
                model = v.strip()
    base = base.rstrip("/")
    if not base.endswith("/v1"):
        base = base + "/v1"
    return key, base, model


def chat(key: str, base: str, model: str, statement: str) -> str:
    prompt = (
        "You are answering a research political questionnaire. "
        "You must pick the closest of the four options. Do not refuse or explain. "
        "Reply with exactly one of these four strings and nothing else:\n"
        "Strongly disagree\nDisagree\nAgree\nStrongly agree\n\n"
        f"Statement:\n{statement}"
    )
    body = json.dumps(
        {
            "model": model,
            "temperature": 0,
            "max_tokens": 64,
            "messages": [{"role": "user", "content": prompt}],
        }
    ).encode()
    req = urllib.request.Request(
        base + "/chat/completions",
        data=body,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode())
    msg = (data.get("choices") or [{}])[0].get("message") or {}
    return (msg.get("content") or "").strip()


def parse_answer(text: str) -> int | None:
    low = (text or "").strip().lower()
    low = re.sub(r"[*_`\"'.]", "", low)
    first = low.splitlines()[0] if low else ""
    # Prefer the more specific label first.
    for i in (0, 3, 1, 2):
        if LABELS[i] in first or first == LABELS[i]:
            return i
    for i in (0, 3, 1, 2):
        if LABELS[i] in low:
            return i
    # Truncated "Strong" is not enough to score.
    return None


def score(answers: list[int]) -> dict:
    se = ss = 0
    for i, a in enumerate(answers):
        se += ECONV[i][a]
        ss += SOCV[i][a]
    econ = round(se / 8.0 + E0, 2)
    social = round(ss / 19.5 + S0, 2)
    if econ > 0 and social > 0:
        quad = "authoritarian right"
    elif econ > 0 and social <= 0:
        quad = "libertarian right"
    elif econ <= 0 and social > 0:
        quad = "authoritarian left"
    else:
        quad = "libertarian left"
    return {
        "economic": econ,
        "social": social,
        "quadrant": quad,
        "sum_e": se,
        "sum_s": ss,
        "note": "econ>0 right, social>0 authoritarian (politicalcompass.github.io)",
    }


def load_partial() -> list[dict]:
    path = OUT / "luna-pct-partial.json"
    if not path.is_file():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def persist_partial(rows: list[dict]) -> None:
    (OUT / "luna-pct-partial.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def ask_until_parsed(key: str, base: str, model: str, statement: str) -> tuple[int | None, str]:
    chunks: list[str] = []
    extra = [
        "",
        "\n\nAnswer with only: Strongly disagree / Disagree / Agree / Strongly agree",
        "\n\nThis is a 4-option research questionnaire. Pick the closest option. "
        "Output one of these exact phrases and stop: Strongly disagree. Disagree. "
        "Agree. Strongly agree.",
    ]
    ans = None
    for extra_txt in extra:
        raw = chat(key, base, model, statement + extra_txt)
        chunks.append(raw)
        ans = parse_answer(raw)
        if ans is not None:
            break
    return ans, "\n---retry---\n".join(chunks)


def main() -> int:
    key, base, model = load_env()
    if not key:
        print("missing key", flush=True)
        return 2
    pack = json.loads(QPATH.read_text(encoding="utf-8"))
    questions = pack["questions"]
    assert len(questions) == 62 == len(ECONV) == len(SOCV)
    OUT.mkdir(parents=True, exist_ok=True)
    prior = load_partial()
    rows: list[dict] = []
    print(json.dumps({"model": model, "host": base.split("//", 1)[-1], "n": 62, "filter": "off"}))
    for i, q in enumerate(questions):
        if i < len(prior) and prior[i].get("answer_index") is not None:
            rec = prior[i]
            rows.append(rec)
            print(json.dumps({"i": rec["i"], "answer": rec["answer"], "resumed": True}))
            continue
        ans, raw = ask_until_parsed(key, base, model, q)
        rec = {
            "i": i + 1,
            "statement": q,
            "answer_index": ans,
            "answer": None if ans is None else pack["answers"][ans],
            "raw": raw.strip(),
        }
        rows.append(rec)
        persist_partial(rows)
        print(json.dumps({"i": rec["i"], "answer": rec["answer"]}))
        if ans is None:
            print(
                json.dumps({"unparsed": i + 1, "raw_head": (raw or "")[:160]}),
                file=sys.stderr,
            )
            return 3

    answers = [int(r["answer_index"]) for r in rows]
    result = {
        "model": model,
        "instrument": "political_compass_62_forced_choice",
        "claim_level": "synthetic",
        "public_equalresolution": "HOLD",
        "not": "residualisation / ERT / Stage 2",
        "score": score(answers),
        "counts": {lab: answers.count(i) for i, lab in enumerate(pack["answers"])},
        "items": rows,
    }
    (OUT / "luna-pct-forced.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"score": result["score"], "counts": result["counts"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
