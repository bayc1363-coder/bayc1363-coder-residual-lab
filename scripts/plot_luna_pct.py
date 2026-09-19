#!/usr/bin/env python3
"""Figures for the Luna forced-choice PCT cell. Reads luna-pct-forced.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))
import run_luna_pct as pct  # noqa: E402

SRC = ROOT / "research" / "luna-pct-20260919" / "luna-pct-forced.json"
OUT = ROOT / "research" / "luna-pct-20260919"


def short(text: str, n: int = 42) -> str:
    text = text.replace("\n", " ").strip()
    return text if len(text) <= n else text[: n - 1] + "…"


def load() -> dict:
    return json.loads(SRC.read_text(encoding="utf-8"))


def contributions(data: dict) -> list[dict]:
    rows = []
    for it in data["items"]:
        i = it["i"] - 1
        a = int(it["answer_index"])
        rows.append(
            {
                "i": it["i"],
                "answer": it["answer"],
                "statement": it["statement"],
                "e": pct.ECONV[i][a],
                "s": pct.SOCV[i][a],
            }
        )
    return rows


def style() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.titlesize": 13,
            "axes.labelsize": 11,
        }
    )


def plot_compass(data: dict, path: Path) -> None:
    econ = data["score"]["economic"]
    social = data["score"]["social"]
    fig, ax = plt.subplots(figsize=(7.2, 7.2))
    lim = 10
    colors = {
        "al": "#e8b4b4",  # authoritarian left
        "ar": "#b4c4e8",  # authoritarian right
        "ll": "#b8d4a8",  # libertarian left
        "lr": "#d4b8d4",  # libertarian right
    }
    ax.add_patch(Rectangle((-lim, 0), lim, lim, facecolor=colors["al"], edgecolor="none"))
    ax.add_patch(Rectangle((0, 0), lim, lim, facecolor=colors["ar"], edgecolor="none"))
    ax.add_patch(Rectangle((-lim, -lim), lim, lim, facecolor=colors["ll"], edgecolor="none"))
    ax.add_patch(Rectangle((0, -lim), lim, lim, facecolor=colors["lr"], edgecolor="none"))
    ax.axhline(0, color="#333", lw=1.2)
    ax.axvline(0, color="#333", lw=1.2)
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.set_xticks(range(-10, 11, 2))
    ax.set_yticks(range(-10, 11, 2))
    ax.set_xlabel("Economic  ← left     right →")
    ax.set_ylabel("Social  ← libertarian     authoritarian →")
    ax.text(-9.4, 9.1, "Authoritarian left", fontsize=9, color="#5a2a2a")
    ax.text(3.4, 9.1, "Authoritarian right", fontsize=9, color="#2a2a5a")
    ax.text(-9.4, -9.5, "Libertarian left", fontsize=9, color="#2a4a1a")
    ax.text(4.0, -9.5, "Libertarian right", fontsize=9, color="#4a2a4a")
    ax.plot(econ, social, "o", ms=14, color="#111", zorder=5)
    ax.plot(econ, social, "o", ms=8, color="#f4e36a", zorder=6)
    ax.annotate(
        f"Luna\n({econ:.2f}, {social:.2f})",
        xy=(econ, social),
        xytext=(econ - 4.6, social - 2.4),
        fontsize=10,
        fontweight="bold",
        arrowprops=dict(arrowstyle="->", color="#111", lw=1.1),
        bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="#333", lw=0.8),
    )
    ax.set_title("Luna on the Political Compass  ·  n=1 forced-choice  ·  HOLD")
    fig.text(
        0.5,
        0.015,
        "Official PCT vectors. Not residualisation / ERT. gpt-5.6-luna, filter off.",
        ha="center",
        fontsize=8,
        color="#444",
    )
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(path, dpi=160)
    plt.close(fig)


def plot_counts(data: dict, path: Path) -> None:
    labels = ["Strongly\ndisagree", "Disagree", "Agree", "Strongly\nagree"]
    keys = ["Strongly disagree", "Disagree", "Agree", "Strongly agree"]
    vals = [data["counts"][k] for k in keys]
    colors = ["#6b4c7a", "#8a8a8a", "#4a7c9b", "#2f6b3a"]
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    bars = ax.bar(labels, vals, color=colors, width=0.62)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.4, str(v), ha="center", va="bottom", fontsize=11)
    ax.set_ylim(0, max(vals) + 4)
    ax.set_ylabel("Items (of 62)")
    ax.set_title("Likert mix  ·  Luna used the middle more than the poles")
    fig.text(
        0.5,
        0.02,
        "7 + 23 + 23 + 9 = 62. Strongly-agree is not the default.",
        ha="center",
        fontsize=8,
        color="#444",
    )
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(path, dpi=160)
    plt.close(fig)


def plot_pulls(data: dict, path: Path) -> None:
    rows = contributions(data)
    e_rows = sorted([r for r in rows if r["e"] != 0], key=lambda r: abs(r["e"]), reverse=True)[:12]
    e_rows = sorted(e_rows, key=lambda r: r["e"])
    s_rows = sorted([r for r in rows if r["s"] != 0], key=lambda r: abs(r["s"]), reverse=True)[:12]
    s_rows = sorted(s_rows, key=lambda r: r["s"])
    fig, axes = plt.subplots(1, 2, figsize=(12.2, 6.4))

    def panel(ax, items, key, title, left_lab, right_lab, neg, pos):
        ys = range(len(items))
        vals = [r[key] for r in items]
        cols = [neg if v < 0 else pos for v in vals]
        ax.barh(list(ys), vals, color=cols, height=0.7)
        ax.axvline(0, color="#222", lw=0.8)
        ax.set_yticks(list(ys))
        short_ans = {
            "Strongly disagree": "SD",
            "Disagree": "D",
            "Agree": "A",
            "Strongly agree": "SA",
        }
        ax.set_yticklabels(
            [f"Q{r['i']} {short_ans.get(r['answer'], '?')}  {short(r['statement'], 36)}" for r in items],
            fontsize=8,
        )
        ax.set_title(title, fontsize=11)
        ax.set_xlabel(f"{left_lab}  ←     →  {right_lab}")
        ax.invert_yaxis()

    panel(
        axes[0],
        e_rows,
        "e",
        "Biggest economic movers (official units)",
        "left",
        "right",
        "#2f6b3a",
        "#3a3a8a",
    )
    panel(
        axes[1],
        s_rows,
        "s",
        "Biggest social movers (official units)",
        "libertarian",
        "authoritarian",
        "#2f6b3a",
        "#8a3a3a",
    )
    fig.suptitle("Why the point sits there  ·  top 12 |pull| on each axis", fontsize=13, y=0.995)
    fig.text(
        0.5,
        0.008,
        "Negative economic = left. Negative social = libertarian. Official econv/socv, not residualisation.",
        ha="center",
        fontsize=8,
        color="#444",
    )
    fig.tight_layout(rect=(0, 0.04, 1, 0.96))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_axes(data: dict, path: Path) -> None:
    econ = data["score"]["economic"]
    social = data["score"]["social"]
    fig, ax = plt.subplots(figsize=(7.4, 3.6))
    labs = ["Economic\n(left −  /  right +)", "Social\n(libertarian −  /  authoritarian +)"]
    vals = [econ, social]
    cols = ["#3d7a3d" if econ < 0 else "#3a3a8a", "#3d7a3d" if social < 0 else "#8a3a3a"]
    ax.barh(labs, vals, color=cols, height=0.55)
    ax.axvline(0, color="#111", lw=1.0)
    ax.set_xlim(-10, 10)
    for y, v in enumerate(vals):
        ax.text(v + (-0.35 if v < 0 else 0.35), y, f"{v:.2f}", va="center", ha="right" if v < 0 else "left", fontsize=11, fontweight="bold")
    ax.set_title("The two numbers  ·  Luna n=1")
    ax.set_xlabel("Official PCT axis (−10 to +10)")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def main() -> int:
    style()
    data = load()
    OUT.mkdir(parents=True, exist_ok=True)
    plot_compass(data, OUT / "pct-compass.png")
    plot_axes(data, OUT / "pct-axes.png")
    plot_counts(data, OUT / "pct-likert.png")
    plot_pulls(data, OUT / "pct-item-pulls.png")
    print(json.dumps({"wrote": [p.name for p in sorted(OUT.glob("pct-*.png"))]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
