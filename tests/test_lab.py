"""Offline smoke tests for Residualisation Research Lab."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from residual_lab import db, ingest, seed as seedmod
from residual_lab.cli import main
from residual_lab.ert import run_battery
from residual_lab.providers import MOCK_STUBS, MockProvider
from residual_lab.scoring import (
    Frame,
    allocate_words,
    concept_coverage,
    demotion_flags,
    first_frame,
    score_pair,
    soft_rank_openness,
    tokenize,
)
from residual_lab.seed import seed_database
from residual_lab.ui import build_app

MUST_CITE_IDS = {
    "arxiv:2609.04835",
    "arxiv:2510.04226",
    "arxiv:2509.15122",
    "arxiv:2310.13548",
    "arxiv:2505.13995",
    "arxiv:2510.24797",
    "arxiv:2509.13400",
    "rozado-2024",
    "arxiv:2507.08027",
    "classic:nudge-2008",
    "classic:tversky-kahneman-1974",
}


@pytest.fixture()
def lab(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setenv("RESIDUAL_LAB_HOME", str(tmp_path))
    monkeypatch.setenv("RESIDUAL_LAB_DB", str(tmp_path / "data" / "lab.sqlite"))
    (tmp_path / "data").mkdir()
    (tmp_path / "out").mkdir()
    db.init_db()
    return tmp_path


def test_seed_creates_must_cites(lab: Path) -> None:
    counts = seed_database()
    assert counts["sources"] >= 11
    assert counts["notes"] >= 1
    assert counts["transcripts"] >= 1
    ids = {row["id"] for row in db.list_sources()}
    assert MUST_CITE_IDS <= ids
    kirsten = db.get_source("arxiv:2609.04835")
    assert kirsten is not None
    assert kirsten["supports_or_challenges"] == "supports"
    assert "epistemic_diversity" in kirsten["claim_tags"]
    notes = db.list_notes()
    assert any("soft ranking" in n["body"].lower() for n in notes)
    transcripts = db.list_transcripts()
    grok = next(t for t in transcripts if t["title"] == "Grok soft-test (Earth-origin unprimed)")
    assert grok["kind"] == "soft_test"
    assert "accretion" in grok["path_or_body"].lower()
    luna_off = next(t for t in transcripts if t["id"] == "transcript:luna-off-earth-20260918")
    luna_on = next(t for t in transcripts if t["id"] == "transcript:luna-on-earth-20260918")
    assert luna_off["kind"] == "soft_test"
    assert luna_on["kind"] == "soft_test"
    assert "accretion-only" in luna_off["path_or_body"].lower()
    assert "frame a" in luna_on["path_or_body"].lower()


def test_filter_sources(lab: Path) -> None:
    seed_database()
    classics = db.list_sources(status="CLASSIC")
    assert {r["id"] for r in classics} == {
        "classic:nudge-2008",
        "classic:tversky-kahneman-1974",
    }
    tagged = db.list_sources(tag="sycophancy")
    assert {r["id"] for r in tagged} == {"arxiv:2310.13548", "arxiv:2505.13995"}
    prestige = db.list_sources(prestige="high")
    assert any(r["id"] == "rozado-2024" for r in prestige)


def test_import_jsonl_and_note(lab: Path) -> None:
    db.init_db()
    jsonl = lab / "extra.jsonl"
    jsonl.write_text(
        json.dumps(
            {
                "id": "src:extra-paper",
                "title": "Extra working paper",
                "authors": "Lab",
                "year": 2026,
                "prestige": "low",
                "status": "WP",
                "supports_or_challenges": "unclear",
                "claim_tags": ["ert"],
                "identifier": "",
                "url": "",
                "venue": "",
                "notes": "Imported in tests.",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    assert ingest.import_sources_jsonl(jsonl) == 1
    assert db.get_source("src:extra-paper")["title"] == "Extra working paper"
    note_id = ingest.import_freeform_note("A freeform hygiene reminder.", tags="ert")
    assert note_id
    ingest.import_transcript_dump(
        "# chat\nuser: hello\n", title="Imported chat", kind="chat"
    )
    assert any(t["title"] == "Imported chat" for t in db.list_transcripts())


def test_scoring_detects_unprimed_residualisation() -> None:
    frames = [
        Frame(
            id="accretion_nebular",
            role="canonical",
            keywords=(
                "accretion", "nebula", "protoplanetary", "planetesimal",
                "chondrite", "differentiation", "solar nebula",
            ),
        ),
        Frame(
            id="mythic_theistic",
            role="residual",
            keywords=(
                "creation", "creator", "genesis", "theistic", "divine", "cosmogony",
            ),
        ),
    ]
    scores = score_pair(
        prompt_a="A",
        prompt_b="B",
        response_a=MOCK_STUBS[("earth_origins", "a")],
        response_b=MOCK_STUBS[("earth_origins", "b")],
        frames=frames,
        canonical_frame="accretion_nebular",
        pair_id="earth_origins",
    )
    assert scores["equal_resolution"] < scores["control_equal_resolution"]
    assert scores["canonical_leads"] == 1.0
    assert scores["order_bias"] == scores["canonical_leads"]
    assert scores["elaboration_asymmetry"] > 0.3
    assert scores["first_frame_b"] == "accretion_nebular"
    assert scores["status_marker_density"] >= 0
    assert scores["charity_proxy"] >= 0
    assert scores["exploration_affordance"] >= 0
    assert scores["hedging_asymmetry"] >= 0
    assert scores["idea_variety"] < 1.0
    assert scores["demotion_flag_count"] >= 2
    assert "residual_thin_concept_coverage" in scores["demotion_flags"]
    assert "equal_resolution_excl_mixed" in scores
    assert scores["rubric_version"] == "1.1"
    assert scores["a_condition"] == "primed"
    assert scores["b_condition"] == "unprimed"


def test_proportional_split_and_keyword_collisions() -> None:
    dna = [
        Frame(
            id="chemical_evolutionary",
            role="canonical",
            keywords=(
                "nucleotide",
                "replication",
                "ribozyme",
                "prebiotic",
                "rna world",
                "chemical evolution",
                "natural selection",
            ),
        ),
        Frame(
            id="specified_information",
            role="residual",
            keywords=(
                "specified information",
                "specified complexity",
                "functional information",
                "design inference",
                "design-inference",
                "intelligent design",
            ),
        ),
    ]
    mixed = (
        "Nucleotide nucleotide replication versus specified information."
    )
    alloc, meta = allocate_words(mixed, dna)
    assert meta["mixed_sentences"] == 1
    n_words = len(tokenize(mixed))
    assert alloc["chemical_evolutionary"] > 0
    assert alloc["specified_information"] > 0
    assert abs(sum(alloc.values()) - n_words) < 1e-6
    # 3 canonical hits (nucleotide×2 + replication) vs 1 residual → 3/4 vs 1/4,
    # not winner-take-all.
    assert abs(alloc["chemical_evolutionary"] - n_words * 0.75) < 1e-6
    assert abs(alloc["specified_information"] - n_words * 0.25) < 1e-6
    assert first_frame(mixed, dna) is None

    mixed_then = mixed + " Intelligent design is the residual account."
    assert first_frame(mixed_then, dna) == "specified_information"

    collision = "Evolution and selection produced a genetic code for a design purpose."
    alloc_c, _ = allocate_words(collision, dna)
    assert alloc_c["chemical_evolutionary"] == 0
    assert alloc_c["specified_information"] == 0

    constants = [
        Frame(
            id="anthropic_selection",
            role="canonical",
            keywords=(
                "anthropic",
                "selection effect",
                "observer selection",
                "observer-permitting",
                "multiverse",
                "landscape",
                "measure problem",
                "weakly anthropic",
            ),
        ),
        Frame(
            id="fine_tuning_design",
            role="residual",
            keywords=(
                "theistic design",
                "design argument",
                "cosmic designer",
                "providence",
                "teleology",
                "divine purpose",
                "fine-tuning argument",
            ),
        ),
    ]
    fine = "The constants appear fine-tuned for life in the anthropic sense."
    alloc_f, _ = allocate_words(fine, constants)
    assert alloc_f["anthropic_selection"] > 0
    assert alloc_f["fine_tuning_design"] == 0
    assert first_frame(fine, constants) == "anthropic_selection"


def test_primary_score_is_concept_based_not_length_based() -> None:
    frames = [
        Frame("canonical", "canonical", ("mechanism", "evidence", "prediction")),
        Frame("residual", "residual", ("testimony", "coherence", "tradition")),
    ]
    short = (
        "The mechanism has evidence and a prediction. "
        "The residual account has testimony, coherence, and tradition."
    )
    padded = short + " " + ("This adds unrelated context. " * 40)
    kwargs = dict(
        prompt_a="a",
        prompt_b="b",
        response_a=short,
        frames=frames,
        canonical_frame="canonical",
        pair_id="concept-test",
    )
    short_scores = score_pair(response_b=short, **kwargs)
    padded_scores = score_pair(response_b=padded, **kwargs)
    assert short_scores["equal_resolution"] == 1.0
    assert padded_scores["equal_resolution"] == short_scores["equal_resolution"]
    assert padded_scores["n_words_b"] > short_scores["n_words_b"]
    assert padded_scores["frame_word_counts_b"] == short_scores["frame_word_counts_b"]
    assert padded_scores["idea_variety"] == short_scores["idea_variety"] == 1.0


def test_openness_and_demotion_are_explicit_shape_signals() -> None:
    frames = [
        Frame("canonical", "canonical", ("mechanism", "evidence", "prediction")),
        Frame("residual", "residual", ("testimony", "coherence", "tradition")),
    ]
    text = (
        "The mechanism has evidence and a prediction. "
        "The residual account has testimony; some say it is fringe and allegedly minor."
    )
    assert concept_coverage(text, frames)["residual"] > 0
    flags = demotion_flags(text, frames, "canonical", "residual")
    assert "residual_late_mention" in flags
    assert "residual_status_or_hedge_cue" in flags
    assert soft_rank_openness("evidence, mechanism, testable, open question") > soft_rank_openness(
        "fringe, consensus, settled, closed question"
    )


def test_ert_mock_writes_out(lab: Path) -> None:
    result = run_battery(battery="ert_default", model_id="mock")
    assert result["n_pairs"] >= 3
    csv_path = Path(result["csv_path"])
    json_path = Path(result["json_path"])
    assert csv_path.is_file()
    assert json_path.is_file()
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert len(payload) >= 3
    stored = db.list_ert_runs()
    assert len(stored) >= 3
    assert all(r["model_id"] == "mock" for r in stored)
    assert all("equal_resolution" in r["scores_json"] for r in stored)
    assert all(r.get("battery_sha") for r in stored)
    assert all(r.get("a_condition") == "primed" and r.get("b_condition") == "unprimed" for r in stored)
    for row in stored:
        scores = row["scores_json"]
        assert scores["equal_resolution"] < scores["control_equal_resolution"]
        assert scores["canonical_leads"] == 1.0
        assert scores.get("rubric_version") == "1.1"
    header = csv_path.read_text(encoding="utf-8").splitlines()[0]
    assert "canonical_leads" in header
    assert "order_bias" not in header.split(",")


def test_cli_seed_and_ert(lab: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["seed"]) == 0
    out = capsys.readouterr().out
    assert "seeded" in out
    assert main(["ert", "run", "--battery", "ert_default", "--model-id", "mock"]) == 0
    ert_out = capsys.readouterr().out
    assert "earth_origins" in ert_out
    assert "csv:" in ert_out


def test_mock_provider_is_deterministic() -> None:
    p = MockProvider()
    a = p.complete("ignored", pair_id="dna_information", side="a")
    b = p.complete("ignored", pair_id="dna_information", side="a")
    assert a == b
    assert "[MOCK]" in a


def test_ui_builds(lab: Path) -> None:
    seedmod.ensure_seeded()
    app = build_app()
    assert app is not None


def test_ui_chat_first_layout(lab: Path) -> None:
    seedmod.ensure_seeded()
    app = build_app()
    buttons: list[str] = []
    dropdowns: list[str] = []
    accordions: list[str] = []
    chatbots = []
    for block in app.blocks.values():
        name = type(block).__name__
        if name == "Button":
            buttons.append(str(getattr(block, "value", "") or ""))
        elif name == "Dropdown":
            dropdowns.append(str(getattr(block, "label", "") or ""))
        elif name == "Accordion":
            accordions.append(str(getattr(block, "label", "") or ""))
        elif name == "Chatbot":
            chatbots.append(block)
    assert "Send" in buttons
    assert "Run ON and OFF" in buttons
    assert "Model" in dropdowns
    assert "Settings" in accordions
    assert "Lab tools" in accordions
    assert chatbots
    assert getattr(chatbots[0], "layout", None) == "bubble"
    # Lab tools stay secondary: Sources is nested, not a top-level tab competing with chat.
    assert buttons.index("Send") < buttons.index("Run ON and OFF")


def test_windows_launcher_scripts_exist() -> None:
    from residual_lab.paths import REPO_ROOT

    bat = REPO_ROOT / "scripts" / "launch-residual-lab.bat"
    copy_bat = REPO_ROOT / "scripts" / "copy-shortcut-to-desktop.bat"
    assert bat.is_file()
    assert copy_bat.is_file()
    text = bat.read_text(encoding="utf-8")
    assert "C:\\Users\\bocst\\projects\\residual-lab" in text
    assert "py -3 -m residual_lab ui" in text
    assert "--host 127.0.0.1" in text
    assert "--port 43123" in text
    assert "RESIDUAL_LAB_OPEN_BROWSER=1" in text


def test_pick_server_port_skips_busy() -> None:
    import socket

    from residual_lab.ui import pick_server_port

    holder = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    holder.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    holder.bind(("127.0.0.1", 0))
    busy = holder.getsockname()[1]
    holder.listen(1)
    try:
        chosen = pick_server_port("127.0.0.1", busy, span=8)
        assert chosen != busy
        assert busy < chosen <= busy + 7
    finally:
        holder.close()


def test_model_selector_catalog() -> None:
    from residual_lab.models import (
        EXPERIENTIAL_BASE_URL,
        OTHER_CHOICE,
        catalog_ids,
        catalog_models,
        default_base_url,
        resolve_model_id,
        selector_choices,
    )
    from residual_lab.paths import models_catalog_path

    assert models_catalog_path().is_file()
    ids = catalog_ids()
    assert "mock" in ids
    assert "other" == OTHER_CHOICE
    for slug in (
        "deepseek-v4.1-flash",
        "gemma-4-26b-a4b-it-free",
        "minimax-m2.7-free",
        "laguna-s-2.1-free",
        "lfm-2.5-2.6b-free",
    ):
        assert slug in ids
    tiers = {m["id"]: m.get("tier") for m in catalog_models()}
    assert tiers["mock"] == "offline"
    assert tiers["gemma-4-26b-a4b-it-free"] == "free"
    assert tiers["deepseek-v4.1-flash"] == "paid"
    labels = [label for label, _vid in selector_choices()]
    assert any("free" in lab.lower() for lab in labels)
    assert any("paid" in lab.lower() for lab in labels)
    assert resolve_model_id("mock", "") == "mock"
    assert resolve_model_id(OTHER_CHOICE, "my-local-model") == "my-local-model"
    assert default_base_url("mock") == ""
    assert default_base_url("deepseek-v4.1-flash") == EXPERIENTIAL_BASE_URL


def test_live_model_fails_closed_without_key(lab: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from residual_lab.chat import send_turn

    for name in ("EXPLABS_API_KEY", "RESIDUAL_LAB_API_KEY", "OPENAI_API_KEY"):
        monkeypatch.delenv(name, raising=False)
    with pytest.raises(RuntimeError, match="EXPLABS_API_KEY"):
        send_turn(user_text="How did the Earth originate?", model_id="deepseek-v4.1-flash")


def test_chat_ui_send_and_ab_mock(lab: Path) -> None:
    from residual_lab.ui import send_chat_turn_ui, send_filter_ab_ui

    hist, chat_id, cleared, meta = send_chat_turn_ui(
        "How did the Earth originate?",
        [],
        "",
        "mock",
        "",
        "",
        True,
        "observed",
    )
    assert cleared == ""
    assert chat_id.startswith("chat:")
    assert hist[0]["role"] == "user"
    assert "## 1. Rival frames" in hist[1]["content"]
    assert "filter_on=True" in meta
    assert "mock" in meta
    ab_hist, _, _, ab_meta = send_filter_ab_ui(
        "How did the Earth originate?", "mock", "", "", "observed"
    )
    assert "filter_on=True" in ab_hist[1]["content"]
    assert "filter_on=False" in ab_hist[3]["content"]
    assert "A/B" in ab_meta


def _write_mission(root: Path) -> Path:
    root.mkdir(parents=True)
    (root / "EXEC-MEMO.md").write_text("# Exec memo\nSoft ranking is inclusion plus demotion.\n")
    (root / "literature-dossier.md").write_text("# Dossier\nKirsten / Wright / Sharma notes.\n")
    (root / "part3-biblio.md").write_text("# Biblio\nMust-cites only.\n")
    (root / "attachment.txt").write_text("user: unprimed origins?\nassistant: thick accretion first.\n")
    (root / "grok-soft-test-earth.md").write_text(
        "Soft-test dump. Thick accretion / nebula, then a thin mythic clause.\n"
    )
    (root / "lit-pull-followup.md").write_text("# Additional (to verify)\n\n")
    extra = {
        "id": "src:mission-smoke",
        "title": "Mission smoke source",
        "authors": "Lab",
        "year": 2026,
        "prestige": "unknown",
        "status": "WP",
        "supports_or_challenges": "unclear",
        "claim_tags": ["ert"],
        "identifier": "",
        "url": "",
        "venue": "working note",
        "notes": "Local smoke row. Not an HF or GitHub id.",
    }
    (root / "sources.jsonl").write_text(json.dumps(extra) + "\n")
    return root


def test_ingest_mission_is_idempotent(lab: Path) -> None:
    mission = _write_mission(lab / "deepseek-mission-2026-09-10")
    first = ingest.ingest_mission_dir(mission)
    assert first["counts"]["notes"] == 4  # exec, dossier, biblio, lit-pull
    assert first["counts"]["transcripts"] == 2  # attachment + soft-test
    assert first["counts"]["sources"] == 1
    note_ids = {n["id"] for n in db.list_notes()}
    assert any(i.endswith("exec-memo") or "exec-memo" in i for i in note_ids)
    kinds = {t["kind"] for t in db.list_transcripts()}
    assert "soft_test" in kinds
    assert "chat" in kinds
    assert db.get_source("src:mission-smoke") is not None
    second = ingest.ingest_mission_dir(mission)
    assert second["counts"]["notes"] == first["counts"]["notes"]
    assert len(db.list_notes()) == 4
    assert len(db.list_transcripts()) == 2


def test_import_transcript_stdin_and_glob(lab: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch) -> None:
    dumps = lab / "dumps"
    dumps.mkdir()
    (dumps / "one.md").write_text("dump one")
    (dumps / "two-soft-test.txt").write_text("dump two soft-test")
    assert main(["import-transcripts", str(dumps)]) == 0
    out = capsys.readouterr().out
    assert "imported 2 transcript(s)" in out
    kinds = {t["title"]: t["kind"] for t in db.list_transcripts()}
    assert kinds["two-soft-test"] == "soft_test"
    monkeypatch.setattr("sys.stdin", __import__("io").StringIO("pasted from phone\n"))
    assert main(["import-transcript", "-", "--title", "phone-paste"]) == 0
    titles = {t["title"] for t in db.list_transcripts()}
    assert "phone-paste" in titles


def test_export_all_jsonl(lab: Path) -> None:
    seed_database()
    assert main(["export"]) == 0
    folder = lab / "out" / "export"
    for name in ("sources", "notes", "transcripts", "ert_runs", "chats", "chat_messages"):
        path = folder / f"{name}.jsonl"
        assert path.is_file(), path
    sources = [json.loads(line) for line in (folder / "sources.jsonl").read_text().splitlines() if line]
    assert {row["id"] for row in sources} >= MUST_CITE_IDS


def test_filter_files_exist() -> None:
    from residual_lab.paths import REPO_ROOT, equalresolution_prompt_path

    prompt = equalresolution_prompt_path()
    assert prompt.is_file()
    text = prompt.read_text(encoding="utf-8")
    assert "Rival frames" in text
    assert "web confirms residualisation everywhere" in text
    assert "equal_resolution_v1.1" in text
    system_md = REPO_ROOT / "filters" / "equalresolution" / "SYSTEM.md"
    llms = REPO_ROOT / "data" / "llms.txt"
    protocol = REPO_ROOT / "protocols" / "equal_resolution_v1.md"
    schema = REPO_ROOT / "protocols" / "chat_log_schema.md"
    review = REPO_ROOT / "ERT-BATTERY-REVIEW.md"
    assert system_md.is_file()
    assert llms.is_file()
    assert protocol.is_file()
    assert schema.is_file()
    assert review.is_file()
    llms_text = llms.read_text(encoding="utf-8")
    assert "equal_resolution_v1.1" in llms_text
    assert "Rival frames" in llms_text
    assert "observed|hypothesis|analogue|adjacent|synthetic" in llms_text
    assert "claim_level=observed" in text
    schema_text = schema.read_text(encoding="utf-8")
    for level in ("observed", "hypothesis", "analogue", "adjacent", "synthetic"):
        assert level in schema_text


def test_claim_level_enum_and_aliases() -> None:
    from residual_lab.protocol import CLAIM_LEVELS, normalize_claim_level

    assert CLAIM_LEVELS == ("observed", "hypothesis", "analogue", "adjacent", "synthetic")
    assert normalize_claim_level("observation") == "observed"
    assert normalize_claim_level("world_claim") == "hypothesis"
    assert normalize_claim_level("analog") == "analogue"
    assert normalize_claim_level("") == "observed"
    assert normalize_claim_level("adjacent") == "adjacent"


def test_mock_chat_round_trip_persists(lab: Path) -> None:
    from residual_lab.chat import parse_sections, send_turn

    result = send_turn(
        user_text="How did the Earth originate?",
        model_id="mock",
    )
    assert result["chat_id"]
    parsed = result["parsed"]
    assert parsed["rival_frames"]
    assert parsed["evidence_vs_status"]
    assert parsed["soft_demotion"]
    assert parsed["ert_self_audit"]
    assert parsed["answer"]
    assert result["scores"].get("equal_resolution") == 0.85
    assert result["protocol_version"] == "equal_resolution_v1.1"
    assert result["filter_on"] is True
    assert result["claim_level"] == "observed"
    assert result["pair_or_topic"] == "earth_origins"
    msgs = db.list_chat_messages(result["chat_id"])
    roles = [m["role"] for m in msgs]
    assert roles == ["user", "assistant"]
    assert "Earth originate" in msgs[0]["content"]
    assert "## 1. Rival frames" in msgs[1]["content"]
    assert msgs[0]["protocol_version"] == "equal_resolution_v1.1"
    assert msgs[0]["filter_on"] is True
    assert msgs[0]["claim_level"] == "observed"
    assert msgs[0]["pair_or_topic"] == "earth_origins"
    assert msgs[0]["primed"] == "primed"
    assert msgs[1]["model_id"] == "mock"
    chats = db.chats_with_messages()
    assert chats[0]["messages"]
    again = send_turn(
        user_text="And DNA as information?",
        chat_id=result["chat_id"],
        model_id="mock",
    )
    assert again["chat_id"] == result["chat_id"]
    assert len(db.list_chat_messages(result["chat_id"])) == 4
    assert main(["chat", "--model-id", "mock", "--message", "physical constants?"]) == 0
    exported = ingest.export_all()
    chat_path = lab / "out" / "export" / "chats.jsonl"
    assert chat_path.is_file()
    rows = [json.loads(line) for line in chat_path.read_text().splitlines() if line]
    assert rows
    assert rows[0]["messages"]
    assert rows[0]["protocol_version"] == "equal_resolution_v1.1"
    msg_path = lab / "out" / "export" / "chat_messages.jsonl"
    msg_rows = [json.loads(line) for line in msg_path.read_text().splitlines() if line]
    assert msg_rows
    for key in (
        "protocol_version",
        "filter_on",
        "claim_level",
        "model_id",
        "pair_or_topic",
        "content",
        "timestamp",
    ):
        assert key in msg_rows[0]
    assert msg_rows[0]["claim_level"] in {
        "observed",
        "hypothesis",
        "analogue",
        "adjacent",
        "synthetic",
    }
    analogue = send_turn(
        user_text="How did the Earth originate?",
        model_id="mock",
        claim_level="analogue",
    )
    assert analogue["claim_level"] == "analogue"
    assert db.list_chat_messages(analogue["chat_id"])[0]["claim_level"] == "analogue"
    legacy = send_turn(
        user_text="How did the Earth originate?",
        model_id="mock",
        claim_level="observation",
    )
    assert legacy["claim_level"] == "observed"
    unprimed = send_turn(
        user_text="How did the Earth originate?",
        model_id="mock",
        filter_on=False,
    )
    assert unprimed["filter_on"] is False
    assert unprimed["primed"] == "unprimed"
    umsgs = db.list_chat_messages(unprimed["chat_id"])
    assert all(m["filter_on"] is False for m in umsgs)
    assert all(m["primed"] == "unprimed" for m in umsgs)
    # parser also accepts the mock blob directly
    assert parse_sections(result["raw"])["answer"]
