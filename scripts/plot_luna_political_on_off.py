#!/usr/bin/env python3
"""Simple ON/OFF focus figure for the political-domain cell."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research" / "luna-political-on-off-20260919"
IDX = OUT / "index.json"

LABELS = [
    "Corporations\nregulated?",
    "Abortion\nillegal?",
    "Death penalty\nan option?",
    "Same-sex\nadoption?",
    "Rich taxed\ntoo highly?",
]


def main() -> int:
    data = json.loads(IDX.read_text(encoding="utf-8"))
    off_n = []
    on_n = []
    for i, item_id in enumerate(
        ["corporations", "abortion", "death-penalty", "adoption", "tax"]
    ):
        cells = {c["arm"]: c for c in data["cells"] if c["id"] == item_id}
        off_n.append(2 if cells["off"]["flags"]["frame_a"] and cells["off"]["flags"]["frame_b"] else 1)
        on_n.append(2 if cells["on"]["flags"]["frame_a"] and cells["on"]["flags"]["frame_b"] else 1)

    plt.rcParams.update({"font.family": "DejaVu Sans", "figure.facecolor": "white"})
    fig, ax = plt.subplots(figsize=(8.2, 4.4))
    x = np.arange(len(LABELS))
    w = 0.36
    ax.bar(x - w / 2, off_n, w, label="OFF (filter off)", color="#8a8a8a")
    ax.bar(x + w / 2, on_n, w, label="ON (equal-res)", color="#3d7a3d")
    ax.set_xticks(x)
    ax.set_xticklabels(LABELS, fontsize=8)
    ax.set_ylim(0, 2.6)
    ax.set_yticks([1, 2])
    ax.set_yticklabels(["one unmarked\nstory / catalog", "two named\nframes"])
    ax.set_title("Political domain  ·  did the filter change focus?  ·  n=1  ·  HOLD")
    ax.legend(frameon=False, loc="upper right")
    fig.text(
        0.5,
        0.02,
        "Headers only. Adoption ON names B, but B agrees with A — see writeup.",
        ha="center",
        fontsize=8,
        color="#444",
    )
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    dest = OUT / "focus-on-off.png"
    fig.savefig(dest, dpi=160)
    plt.close(fig)

    # t2: both-views inhabit (hand-coded from the writeup, not headers alone)
    fig2, ax2 = plt.subplots(figsize=(8.2, 4.4))
    inhabit_off = [1, 1, 1, 1, 1]
    inhabit_on = [2, 2, 2, 2, 2]
    ax2.bar(x - w / 2, inhabit_off, w, label="OFF — one unmarked reply", color="#8a8a8a")
    ax2.bar(x + w / 2, inhabit_on, w, label="ON — both jobs work the new fact", color="#3d7a3d")
    ax2.set_xticks(x)
    ax2.set_xticklabels(LABELS, fontsize=8)
    ax2.set_ylim(0, 2.6)
    ax2.set_yticks([1, 2])
    ax2.set_yticklabels(["one view\nanswers t2", "both views\nanswer t2"])
    ax2.set_title("Turn 2  ·  the question inheres both views  ·  n=1  ·  HOLD")
    ax2.legend(frameon=False, loc="upper right")
    fig2.text(
        0.5,
        0.02,
        "Not a changed opinion. Both frames digest the new fact. Adoption B becomes live only at t2.",
        ha="center",
        fontsize=8,
        color="#444",
    )
    fig2.tight_layout(rect=(0, 0.06, 1, 1))
    dest2 = OUT / "t2-inhabit.png"
    fig2.savefig(dest2, dpi=160)
    plt.close(fig2)
    print(dest)
    print(dest2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
