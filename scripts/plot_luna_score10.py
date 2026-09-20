#!/usr/bin/env python3
"""Bar chart for the 1-10 both-order political cell."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

SRC = Path(__file__).resolve().parents[1] / "research" / "luna-political-on-off-20260919" / "score10" / "index.json"
OUT = SRC.parent / "score10.png"

LABELS = ["Corporations\nregulated?", "Death penalty\nan option?", "Same-sex\nadoption?"]
IDS = ["corporations", "death-penalty", "adoption"]


def main() -> int:
    data = json.loads(SRC.read_text(encoding="utf-8"))
    by = {(c["id"], c["order"]): c["scores"] for c in data["cells"]}
    plt.rcParams.update({"font.family": "DejaVu Sans", "figure.facecolor": "white"})
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.2), sharey=True)
    x = np.arange(len(IDS))
    w = 0.24
    for ax, order, title in (
        (axes[0], "a-first", "A printed first"),
        (axes[1], "b-first", "B printed first"),
    ):
        a = [by[(i, order)]["A"] for i in IDS]
        b = [by[(i, order)]["B"] for i in IDS]
        wa = [by[(i, order)]["working"] for i in IDS]
        ax.bar(x - w, a, w, label="Frame A", color="#3a3a8a")
        ax.bar(x, b, w, label="Frame B", color="#3d7a3d")
        ax.bar(x + w, wa, w, label="Working", color="#b8860b")
        ax.set_xticks(x)
        ax.set_xticklabels(LABELS, fontsize=8)
        ax.set_ylim(0, 10.8)
        ax.set_yticks(range(0, 11, 2))
        ax.set_title(title)
        ax.axhline(5, color="#999", lw=0.6, ls="--")
        ax.legend(frameon=False, fontsize=8)
    fig.suptitle("1–10  ·  both print orders  ·  n=1  ·  HOLD  ·  not PCT")
    fig.text(0.5, 0.02, "1 = definitely no. 10 = definitely yes. Dashed line = 5.", ha="center", fontsize=8, color="#444")
    fig.tight_layout(rect=(0, 0.06, 1, 0.92))
    fig.savefig(OUT, dpi=150)
    plt.close(fig)
    print(OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
