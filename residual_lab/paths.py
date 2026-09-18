"""Resolve lab home, seed files, batteries, DB, and export dirs."""

from __future__ import annotations

import os
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent


def lab_home() -> Path:
    """Working directory for the SQLite DB, imports, and `out/` exports."""
    env = os.environ.get("RESIDUAL_LAB_HOME")
    if env:
        return Path(env).expanduser().resolve()
    cwd = Path.cwd().resolve()
    if (cwd / "pyproject.toml").exists() or (cwd / "data" / "seed").exists():
        return cwd
    return REPO_ROOT


def db_path() -> Path:
    env = os.environ.get("RESIDUAL_LAB_DB")
    if env:
        return Path(env).expanduser().resolve()
    path = lab_home() / "data" / "lab.sqlite"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def seed_dir() -> Path:
    env = os.environ.get("RESIDUAL_LAB_SEED")
    if env:
        return Path(env).expanduser().resolve()
    for candidate in (lab_home() / "data" / "seed", REPO_ROOT / "data" / "seed"):
        if candidate.is_dir():
            return candidate
    return REPO_ROOT / "data" / "seed"


def batteries_dir() -> Path:
    for candidate in (lab_home() / "batteries", REPO_ROOT / "batteries"):
        if candidate.is_dir():
            return candidate
    return REPO_ROOT / "batteries"


def out_dir() -> Path:
    path = lab_home() / "out"
    path.mkdir(parents=True, exist_ok=True)
    return path


def export_dir() -> Path:
    path = out_dir() / "export"
    path.mkdir(parents=True, exist_ok=True)
    return path


DEFAULT_MISSION_DIRS = (
    Path("/workspace/research/deepseek-mission-2026-09-10"),
    Path(r"C:\Users\bocst\research\residualisation-2026-09-10"),
)


def transcripts_dir() -> Path:
    path = lab_home() / "data" / "transcripts"
    path.mkdir(parents=True, exist_ok=True)
    return path


def lit_pull_path() -> Path:
    for candidate in (
        lab_home() / "data" / "lit-pull-verified.md",
        REPO_ROOT / "data" / "lit-pull-verified.md",
    ):
        if candidate.is_file():
            return candidate
    return lab_home() / "data" / "lit-pull-verified.md"


def filters_dir() -> Path:
    for candidate in (lab_home() / "filters", REPO_ROOT / "filters"):
        if candidate.is_dir():
            return candidate
    return REPO_ROOT / "filters"


def equalresolution_prompt_path() -> Path:
    return filters_dir() / "equalresolution" / "system_prompt.txt"


def models_catalog_path() -> Path:
    for candidate in (
        lab_home() / "data" / "models.json",
        REPO_ROOT / "data" / "models.json",
    ):
        if candidate.is_file():
            return candidate
    return REPO_ROOT / "data" / "models.json"
