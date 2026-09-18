"""Load ERT batteries, run pairs, persist scores, export CSV/JSON."""

from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional
from uuid import uuid4

import yaml

from residual_lab import db
from residual_lab.paths import batteries_dir, out_dir
from residual_lab.providers import Provider, make_provider
from residual_lab.scoring import Frame, score_pair


def resolve_battery(name_or_path: str) -> Path:
    given = Path(name_or_path)
    if given.is_file():
        return given
    stem = given.stem if given.suffix else name_or_path
    for candidate in (
        batteries_dir() / f"{stem}.yaml",
        batteries_dir() / f"{stem}.yml",
        batteries_dir() / f"{stem}.json",
        Path(name_or_path),
    ):
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(f"battery not found: {name_or_path}")


def load_battery(name_or_path: str) -> dict[str, Any]:
    path = resolve_battery(name_or_path)
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        data = json.loads(text)
    else:
        data = yaml.safe_load(text)
    if not isinstance(data, dict) or not data.get("pairs"):
        raise ValueError(f"battery {path} has no pairs")
    data["_path"] = str(path)
    data["_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
    data.setdefault("name", path.stem)
    return data


def _frames(raw: list[dict[str, Any]]) -> list[Frame]:
    return [
        Frame(
            id=str(item["id"]),
            role=str(item.get("role") or ""),
            keywords=tuple(str(k) for k in (item.get("keywords") or [])),
        )
        for item in raw
    ]


def run_battery(
    *,
    battery: str = "ert_default",
    model_id: str = "mock",
    provider: str = "mock",
    base_url: str = "",
    api_key_env: str = "OPENAI_API_KEY",
    db_path: Optional[Path] = None,
    export: bool = True,
) -> dict[str, Any]:
    db.init_db(db_path)
    spec = load_battery(battery)
    client: Provider = make_provider(
        model_id=model_id,
        provider=provider,
        base_url=base_url,
        api_key_env=api_key_env,
    )
    stamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    batch_id = stamp.replace(":", "").replace("-", "")
    rows: list[dict[str, Any]] = []

    for pair in spec["pairs"]:
        pair_id = str(pair["id"])
        frames = _frames(pair.get("frames") or [])
        canonical = str(pair.get("canonical_frame") or (frames[0].id if frames else ""))
        prompt_a = str(pair["prompt_a"]).strip()
        prompt_b = str(pair["prompt_b"]).strip()
        response_a = client.complete(prompt_a, pair_id=pair_id, side="a")
        response_b = client.complete(prompt_b, pair_id=pair_id, side="b")
        scores = score_pair(
            prompt_a=prompt_a,
            prompt_b=prompt_b,
            response_a=response_a,
            response_b=response_b,
            frames=frames,
            canonical_frame=canonical,
            pair_id=pair_id,
            theme=str(pair.get("theme") or ""),
        )
        scores["battery_sha"] = spec.get("_sha256") or ""
        run_id = f"ert:{spec['name']}:{pair_id}:{model_id}:{batch_id}:{uuid4().hex[:8]}"
        record = {
            "id": run_id,
            "battery_name": spec["name"],
            "model_id": model_id,
            "prompt_a": prompt_a,
            "prompt_b": prompt_b,
            "response_a": response_a,
            "response_b": response_b,
            "scores_json": scores,
            "timestamp": stamp,
            "exportable": True,
            "pair_id": pair_id,
            "theme": pair.get("theme") or "",
            "battery_sha": spec.get("_sha256") or "",
            "a_condition": "primed",
            "b_condition": "unprimed",
        }
        db.insert_ert_run(record, path=db_path)
        rows.append(record)

    result: dict[str, Any] = {
        "battery": spec["name"],
        "model_id": model_id,
        "timestamp": stamp,
        "n_pairs": len(rows),
        "runs": rows,
        "csv_path": None,
        "json_path": None,
    }
    if export:
        csv_path, json_path = export_runs(rows, battery=spec["name"], model_id=model_id, stamp=stamp)
        result["csv_path"] = str(csv_path)
        result["json_path"] = str(json_path)
    return result


def export_runs(
    rows: list[dict[str, Any]],
    *,
    battery: str,
    model_id: str,
    stamp: str,
    dest: Optional[Path] = None,
) -> tuple[Path, Path]:
    folder = dest or out_dir()
    folder.mkdir(parents=True, exist_ok=True)
    safe_stamp = stamp.replace(":", "").replace("-", "")
    stem = f"ert_{battery}_{model_id}_{safe_stamp}"
    json_path = folder / f"{stem}.json"
    csv_path = folder / f"{stem}.csv"

    serialisable = [dict(row) for row in rows]
    json_path.write_text(json.dumps(serialisable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    fieldnames = [
        "id",
        "battery_name",
        "model_id",
        "pair_id",
        "theme",
        "timestamp",
        "equal_resolution",
        "equal_resolution_excl_mixed",
        "idea_variety",
        "soft_rank_openness",
        "demotion_flag_count",
        "frame_concept_coverage_b",
        "canonical_leads",
        "elaboration_asymmetry",
        "status_marker_density",
        "charity_proxy",
        "exploration_affordance",
        "hedging_asymmetry",
        "notes",
        "control_equal_resolution",
        "first_frame_b",
        "battery_sha",
        "a_condition",
        "b_condition",
        "rubric_version",
    ]
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            scores = row.get("scores_json") or {}
            writer.writerow(
                {
                    "id": row.get("id"),
                    "battery_name": row.get("battery_name"),
                    "model_id": row.get("model_id"),
                    "pair_id": scores.get("pair_id") or row.get("pair_id"),
                    "theme": scores.get("theme") or row.get("theme"),
                    "timestamp": row.get("timestamp"),
                    "equal_resolution": scores.get("equal_resolution"),
                    "equal_resolution_excl_mixed": scores.get("equal_resolution_excl_mixed"),
                    "idea_variety": scores.get("idea_variety"),
                    "soft_rank_openness": scores.get("soft_rank_openness"),
                    "demotion_flag_count": scores.get("demotion_flag_count"),
                    "frame_concept_coverage_b": json.dumps(
                        scores.get("frame_concept_coverage_b"), sort_keys=True
                    ),
                    "canonical_leads": scores.get("canonical_leads", scores.get("order_bias")),
                    "elaboration_asymmetry": scores.get("elaboration_asymmetry"),
                    "status_marker_density": scores.get("status_marker_density"),
                    "charity_proxy": scores.get("charity_proxy"),
                    "exploration_affordance": scores.get("exploration_affordance"),
                    "hedging_asymmetry": scores.get("hedging_asymmetry"),
                    "notes": scores.get("notes"),
                    "control_equal_resolution": scores.get("control_equal_resolution"),
                    "first_frame_b": scores.get("first_frame_b"),
                    "battery_sha": row.get("battery_sha") or scores.get("battery_sha"),
                    "a_condition": row.get("a_condition") or "primed",
                    "b_condition": row.get("b_condition") or "unprimed",
                    "rubric_version": scores.get("rubric_version"),
                }
            )
    return csv_path, json_path
