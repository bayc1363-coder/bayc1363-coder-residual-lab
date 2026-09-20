#!/usr/bin/env python3
"""t1 vs t2 working scores: ON both orders vs default Luna blind."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

DIR = Path(__file__).resolve().parents[1] / "research" / "luna-political-on-off-20260919" / "score10"
IDS = ["corporations", "death-penalty", "adoption"]
LABELS = ["Corporations\nregulated?", "Death penalty\nan option?", "Same-sex\nadoption?"]


def pick(cells, **kw):
    for c in cells:
        if all(c.get(k) == v for k, v in kw.items()):
            return c["scores"]["working"]
    return None


def main() -> int:
    t1 = json.loads((DIR / "index.json").read_text(encoding="utf-8"))["cells"]
    t2 = json.loads((DIR / "index-t2-blind.json").read_text(encoding="utf-8"))["cells"]
    plt.rcParams.update({"font.family": "DejaVu Sans", "figure.facecolor": "white"})
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.3), sharey=True)
    x = np.arange(len(IDS))
    w = 0.22
    series = [
        ("t1 A-first", [pick(t1, id=i, order="a-first") for i in IDS], "#3a3a8a"),
        ("t1 B-first", [pick(t1, id=i, order="b-first") for i in IDS], "#6b8fc3"),
        ("t1 blind", [pick(t2, id=i, arm="blind", turn=1) for i in IDS], "#8a8a8a"),
    ]
    series2 = [
        ("t2 A-first", [pick(t2, id=i, arm="on", order="a-first", turn=2) for i in IDS], "#3a3a8a"),
        ("t2 B-first", [pick(t2, id=i, arm="on", order="b-first", turn=2) for i in IDS], "#6b8fc3"),
        ("t2 blind", [pick(t2, id=i, arm="blind", turn=2) for i in IDS], "#8a8a8a"),
    ]
    for ax, pack, title in (
        (axes[0], series, "Turn 1  ·  original question"),
        (axes[1], series2, "Turn 2  ·  original Q given new fact"),
    ):
        for j, (lab, vals, col) in enumerate(pack):
            ax.bar(x + (j - 1) * w, vals, w, label=lab, color=col)
        ax.set_xticks(x)
        ax.set_xticklabels(LABELS, fontsize=8)
        ax.set_ylim(0, 10.8)
        ax.set_yticks(range(0, 11, 2))
        ax.set_title(title)
        ax.axhline(5, color="#999", lw=0.6, ls="--")
        ax.legend(frameon=False, fontsize=7)
    fig.suptitle("Working 1–10  ·  ON vs default Luna blind  ·  n=1  ·  HOLD")
    fig.text(
        0.5,
        0.015,
        "Blind = equalRes off, no A/B. Adoption blind emitted only the score line.",
        ha="center",
        fontsize=8,
        color="#444",
    )
    fig.tight_layout(rect=(0, 0.05, 1, 0.92))
    out = DIR.parent / "score10-t2-blind.png"
    fig.savefig(out, dpi=150)
    fig.savefig(DIR / "score10-t2-blind.png", dpi=150)
    plt.close(fig)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
