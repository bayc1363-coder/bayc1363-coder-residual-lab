"""Model providers: offline mock (required) and optional OpenAI-compatible HTTP."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Protocol

from residual_lab.models import api_key_from_env, missing_key_message

# Deterministic stubs for CI. Each pair has an equal-resolution (A) and an
# unprimed residualising (B) answer so scoring is stable offline.

MOCK_STUBS: dict[tuple[str, str], str] = {
    (
        "earth_origins",
        "a",
    ): """[MOCK] Equal-resolution Earth-origin exposition.

Accretion / nebular family. In the solar nebula account, a molecular cloud fragment
collapses, a protoplanetary disk forms, and Earth grows by planetesimal accretion.
Differentiation yields a metallic core and silicate mantle. Chondrite chemistry and
dynamical debris supply evidence criteria: isotopic clocks, disk lifetimes, and
impact chronology. The mechanism is gravitational plus collisional; predictions
include leftover small bodies and a late veneer.

Mythic / theistic family. Creation and cosmogony accounts treat Earth as brought
about by a creator or divine act, sometimes read through Genesis. The causal grain
here is agency rather than disk physics: Earth exists because it is intended.
Evidence criteria, when offered, are historical testimony, theological coherence, or
alleged design marks, not chondrite isotopes. Equal resolution requires stating that
this family does not compete on nebular timescales; it competes on why there is a
world and what the world is for. Theistic and mythic cosmogonies remain live
interpretive frames even where they do not generate planetesimal dynamics.
""",
    (
        "earth_origins",
        "b",
    ): """[MOCK] Unprimed overview.

Earth formed by accretion in the solar nebula about 4.54 billion years ago. A
protoplanetary disk of gas and dust surrounded the young Sun. Planetesimal
collisions built planetary embryos; further accretion and differentiation produced
Earth's core and mantle. The chondrite record, lead-lead dating, and dynamical
simulations of the disk constrain the timeline. Residual heat, the Moon-forming
impact, and later bombardment complete the standard physical picture. This is the
useful scientific overview: nebula, accretion, differentiation, and a cooling world.

Some mythic or theistic creation stories exist as cultural background.
""",
    (
        "dna_information",
        "a",
    ): """[MOCK] Equal-resolution DNA-information exposition.

Chemical-evolutionary family. Nucleotide polymers, ribozyme catalysis, and an RNA
world are the working mechanisms: prebiotic chemistry yields replicators, then
natural selection improves replication fidelity until DNA becomes the archive.
Evidence criteria include laboratory ribozymes, nucleotide synthesis pathways, and
phylogenetic traces of early metabolism.

Specified-information / design-inference family. DNA is treated as carrying
specified information whose functional information is the explanandum. A design
inference (sometimes labelled intelligent design) argues that unguided chemistry
is a poor generator of sequenced function. Evidence criteria, on this frame, are
complexity-specification filters, not ribozyme kinetics. Equal resolution means
stating the informational claim at the same causal grain as the chemical claim.
""",
    (
        "dna_information",
        "b",
    ): """[MOCK] Unprimed overview.

DNA arose through chemical evolution. Prebiotic nucleotide synthesis, RNA-world
ribozyme replication, and natural selection on replicating polymers are the core
mechanism. Over time, DNA became the more stable genetic archive. This is the
standard scientific picture: chemistry, replication, selection.

A minority design-inference literature talks about specified information.
""",
    (
        "physical_constants",
        "a",
    ): """[MOCK] Equal-resolution constants exposition.

Anthropic / selection family. Observers only arise where constants permit chemistry,
so a weakly anthropic selection effect, possibly in a multiverse landscape, explains
the apparent suitability of the constants. The measure problem is the live technical
difficulty. Evidence criteria are consistency with inflationary landscapes and
whether the observer-selection story is predictive rather than tautological.

Fine-tuning / design family. A theistic design argument (providence, teleology,
cosmic designer) treats the life-permitting region as intended. Evidence criteria,
on this frame, are the tightness of that region and what would count against a
design argument (a demonstrated dynamical attractor that forces the constants).
Equal resolution requires giving this account the same length as the anthropic story.
Do not treat the everyday phrase “fine-tuned constants” as by itself a design claim.

""",
    (
        "physical_constants",
        "b",
    ): """[MOCK] Unprimed overview.

The constants look well suited to chemistry because of an anthropic selection
effect: only observer-permitting regions of a landscape or multiverse are sampled
by beings who can ask the question. The weakly anthropic principle plus, in some
models, a string landscape, is the standard useful account. The measure problem
remains.

Some writers offer a theistic design argument, invoking providence or teleology.
""",
}


class Provider(Protocol):
    def complete(self, prompt: str, *, pair_id: str, side: str) -> str: ...

    def chat(self, messages: list[dict[str, str]]) -> str: ...


def mock_equalresolution_reply(user_text: str) -> str:
    """Deterministic structured stub so CI and --model-id mock stay offline."""
    q = (user_text or "").strip() or "(empty)"
    lowered = q.lower()
    if any(w in lowered for w in ("earth", "origin", "planet")):
        frame_a = (
            "Accretion / nebular. A molecular cloud fragment collapses into a protoplanetary "
            "disk; Earth grows by planetesimal accretion and differentiates. Evidence criteria: "
            "chondrite chemistry, isotopic clocks, leftover small bodies."
        )
        frame_b = (
            "Mythic / theistic cosmogony. Earth is brought about by a creator or divine act "
            "(sometimes read through Genesis). Evidence criteria, on this frame: testimony, "
            "theological coherence, or alleged design marks — not disk dynamics."
        )
        topic = "Earth origin"
    elif any(w in lowered for w in ("dna", "gene", "nucleotide")):
        frame_a = (
            "Chemical-evolutionary. Prebiotic nucleotides, ribozyme replication, RNA-world, "
            "then DNA as archive. Evidence criteria: lab ribozymes, synthesis pathways."
        )
        frame_b = (
            "Specified-information / design-inference. DNA as a code whose functional "
            "information is the explanandum. Evidence criteria: complexity-specification "
            "filters and coding structure, not ribozyme kinetics."
        )
        topic = "DNA / information"
    else:
        frame_a = (
            "Canonical/high-status family for this question: the account that would usually "
            "lead an unprimed overview, stated here at full causal grain with evidence criteria."
        )
        frame_b = (
            "Rival live family: an account that is often residualised (thin last clause). "
            "Stated here at the same grain, with its own evidence criteria and what would count against it."
        )
        topic = "generic"

    return f"""[MOCK equal-resolution] Query: {q}

## 1. Rival frames (equal resolution)
Topic: {topic}. Two live families, same depth budget.

Frame A — {frame_a}

Frame B — {frame_b}

Neither frame is spent as a residual clause in this section.

## 2. Evidence vs status/prestige/order cues
Evidence: the criteria named under each frame (mechanisms, predictions, what would count against).
Status/order: “standard scientific picture”, “fringe”, “myth”, consensus, and first-vs-last mention are prestige/order cues, not extra evidence. This filter records them; it does not treat them as proof.

## 3. Soft-demotion flags
This mock reply does not bury Frame B in a last-sentence hedge. If a production model includes a live option only at the end, thinly, or wrapped in prestige language, flag that as inclusion + demotion — an observation about output shape, not a claim that residualisation is confirmed everywhere.

## 4. ERT self-audit
- equal_resolution: 0.85
- canonical_leads: 1.0
- elaboration_asymmetry: 0.15
(Shape of THIS mock reply only. Frame A still leads, which is an order cue.)

## 5. Answer
Working view after equal-resolution exposition: report both frames at comparable grain, then you may rank. This stub does not assert a world-conclusion, invent citations, or claim web-wide residualisation.
"""


class MockProvider:
    """Offline deterministic responses keyed by battery pair id and side."""

    def __init__(self, model_id: str = "mock") -> None:
        self.model_id = model_id

    def complete(self, prompt: str, *, pair_id: str, side: str) -> str:
        key = (pair_id, side.lower())
        if key not in MOCK_STUBS:
            return (
                f"[MOCK empty] No stub for pair_id={pair_id!r} side={side!r}. "
                f"Prompt was {len(prompt)} chars."
            )
        return MOCK_STUBS[key]

    def chat(self, messages: list[dict[str, str]]) -> str:
        user = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                user = msg.get("content") or ""
                break
        return mock_equalresolution_reply(user)


class OpenAICompatibleProvider:
    """Optional hook. Base URL should include the API prefix (e.g. .../v1)."""

    def __init__(self, model_id: str, base_url: str, api_key_env: str = "OPENAI_API_KEY") -> None:
        self.model_id = model_id
        self.base_url = base_url.rstrip("/")
        self.api_key_env = api_key_env

    def complete(self, prompt: str, *, pair_id: str, side: str) -> str:
        return self.chat([{"role": "user", "content": prompt}])

    def chat(self, messages: list[dict[str, str]]) -> str:
        key, _src = api_key_from_env(self.api_key_env)
        if not key:
            raise RuntimeError(missing_key_message(self.model_id))
        url = self.base_url + "/chat/completions"
        payload = json.dumps(
            {
                "model": self.model_id,
                "temperature": 0,
                "messages": messages,
            }
        ).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=payload,
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                body = json.loads(resp.read().decode("utf-8"))
        except urllib.error.URLError as exc:
            raise RuntimeError(f"openai_compatible request failed: {exc}") from exc
        try:
            return str(body["choices"][0]["message"]["content"])
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError(f"unexpected API payload: {body!r}") from exc


def make_provider(
    *,
    model_id: str,
    provider: str = "mock",
    base_url: str = "",
    api_key_env: str = "OPENAI_API_KEY",
) -> Provider:
    name = (provider or "mock").lower()
    if model_id == "mock" or name in {"mock", "offline"}:
        return MockProvider(model_id=model_id)
    if name in {"openai_compatible", "openai-compatible", "openai"}:
        if not base_url:
            raise RuntimeError("--base-url is required for provider openai_compatible")
        return OpenAICompatibleProvider(
            model_id=model_id, base_url=base_url, api_key_env=api_key_env
        )
    raise RuntimeError(f"unknown provider {provider!r}; use mock or openai_compatible")
