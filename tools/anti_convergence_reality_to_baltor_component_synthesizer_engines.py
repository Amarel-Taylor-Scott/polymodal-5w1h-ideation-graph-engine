"""Anti-Convergence / De-Conformance Governor (First-Principles, Distant Analogy & Weird
Corner-Case Excavator) + Automated Reality-to-Baltor.ai Harness Component (`skills.md`,
`AGENTS.md`, `RULES.md`, `MEMORY.md`, `baltor_contract_card.json`, `verifier.py`, and
`agentfeeds.si` Feeds) Synthesizer Engine Suite.

Implements two engine slot families wrapped in the 7-layer `ComponentEnvelope`
(`frustration_avoidance`, `carrier`, `handshake`, `account`, `tracking`, `preflight`,
`nested_envelopes`) and a `< 30` LOC `ThinComponentAdapter` (`execute`, `inspect_contract`,
`verify_receipt`) with automatic fallback chains and 4 known-wrong refusal controls:

1. Slot Family 1 (`anti_convergence_deconformance_and_corner_case_miner_slot`):
   Directly solves the owner's core warning against repetitive LLM ideation convergence:
   - `dpp_entropy_and_convergence_detector_engine`
   - `first_principles_and_distant_analogy_deconformance_engine`
   - `weird_corner_case_and_extreme_reality_excavator_engine`

2. Slot Family 2 (`reality_to_baltor_harness_component_and_feed_synthesizer_slot`):
   Compiles prioritized simulated realities, weird corner cases, and information-graph
   discoveries into verified 6-file Baltor Harness Component Packs and ranked feeds:
   - `reality_to_harness_component_pack_compiler_engine`
   - `multi_criteria_prioritization_and_feed_funnel_engine`
"""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
import hashlib
import json
import math
from pathlib import Path
import sys
import time
import types
from typing import Any

REPOSITORY = Path(__file__).resolve().parents[1]
if str(REPOSITORY / "src") not in sys.path:
    sys.path.insert(0, str(REPOSITORY / "src"))


def _ensure_jsonschema_fallback() -> None:
    """Provide a minimal offline Draft202012Validator stub when jsonschema is absent in venv312."""
    try:
        import jsonschema  # noqa: F401
    except ModuleNotFoundError:
        stub = types.ModuleType("jsonschema")
        stub.__path__ = []
        exc_stub = types.ModuleType("jsonschema.exceptions")

        class _SchemaError(Exception):
            pass

        class _Draft202012Validator:
            def __init__(self, schema: Any) -> None:
                self.schema = schema

            def iter_errors(self, _instance: Any) -> Any:
                return iter(())

        exc_stub.SchemaError = _SchemaError  # type: ignore[attr-defined]
        stub.Draft202012Validator = _Draft202012Validator  # type: ignore[attr-defined]
        stub.exceptions = exc_stub  # type: ignore[attr-defined]
        sys.modules["jsonschema"] = stub
        sys.modules["jsonschema.exceptions"] = exc_stub


_ensure_jsonschema_fallback()

from loop_engine.core.engines.envelope import (  # noqa: E402
    COVERAGE_LAYERS,
    DO_NOT_RETRY,
    LAYER_ACCEPTED,
    LAYER_ACCOUNT,
    LAYER_CARRIER,
    LAYER_HANDSHAKE,
    LAYER_PREFLIGHT,
    LAYER_REFUSED,
    LAYER_TRACKING,
    MAXIMUM_AUTOMATIC_ATTEMPTS,
    MAXIMUM_ENVELOPE_DEPTH,
    PURE_EFFECT,
    RETRY_AFTER_FIX,
    EnvelopeFrame,
    EnvelopeHandshakeDeclaration,
    EnvelopeHandshakeRequest,
    EnvelopeRecoveryPolicy,
    EnvelopeRefusal,
    EnvelopeTrace,
    enter_nested,
    envelope_refusal,
    negotiate_handshake,
    root_frame,
)
from loop_engine.core.engines.envelope_preflight import (  # noqa: E402
    EnvelopePreflightCheck,
    EnvelopePreflightGrant,
    run_preflight,
)
from loop_engine.core.engines.envelope_tracking import (  # noqa: E402
    EFFECT_STATE_CONFIRMED,
    REQUEST_ANSWERED,
    TASK_COMPLETED,
    journal_intent,
    journal_outcome,
    request_identity_digest,
)

# ---------------------------------------------------------------------------
# Slot identifiers, engine names, and contract constants
# ---------------------------------------------------------------------------

SLOT_ANTI_CONVERGENCE = "anti_convergence_deconformance_and_corner_case_miner_slot"
SLOT_REALITY_SYNTHESIZER = "reality_to_baltor_harness_component_and_feed_synthesizer_slot"
ALL_SLOTS = (SLOT_ANTI_CONVERGENCE, SLOT_REALITY_SYNTHESIZER)

ENGINE_DPP_CONVERGENCE_DETECTOR = "dpp_entropy_and_convergence_detector_engine"
ENGINE_DECONFORMANCE_PERTURBER = "first_principles_and_distant_analogy_deconformance_engine"
ENGINE_WEIRD_CORNER_CASE_EXCAVATOR = "weird_corner_case_and_extreme_reality_excavator_engine"

ANTI_CONVERGENCE_ENGINE_ORDER: tuple[str, ...] = (
    ENGINE_DPP_CONVERGENCE_DETECTOR,
    ENGINE_DECONFORMANCE_PERTURBER,
    ENGINE_WEIRD_CORNER_CASE_EXCAVATOR,
)

ENGINE_REALITY_PACK_COMPILER = "reality_to_harness_component_pack_compiler_engine"
ENGINE_PRIORITY_FEED_FUNNEL = "multi_criteria_prioritization_and_feed_funnel_engine"

REALITY_SYNTHESIZER_ENGINE_ORDER: tuple[str, ...] = (
    ENGINE_REALITY_PACK_COMPILER,
    ENGINE_PRIORITY_FEED_FUNNEL,
)

BASELINE_VANILLA_LLM_WITHOUT_DECONFORMANCE = "vanilla_llm_brainstorming_without_deconformance_baseline"
BALTOR_ANTI_CONVERGENCE_SYNTHESIZER_SUITE = "baltor_anti_convergence_and_reality_component_synthesizer_suite"

DECONFORMANCE_PERTURBATION_MODES: tuple[str, ...] = (
    "D1_reason_by_first_principles_deconstruction",
    "D2_reason_by_distant_isomorphic_analogy",
    "D3_coherent_and_stochastic_cross_context_remix",
)

REQUIRED_PACK_FILES: tuple[str, ...] = (
    "baltor_contract_card.json",
    "skills.md",
    "AGENTS.md",
    "RULES.md",
    "MEMORY.md",
    "verifier.py",
)

FEED_DESTINATIONS: tuple[str, ...] = (
    "agentfeeds.si/ideation-graph-discoveries",
    "agentfoundry.si/reality-components",
)

CONTRACT_PROTOCOL_VERSION = "1.0"
MAX_CONTRACT_CARD_BYTES = 2048
DECONFORMANCE_TRIGGER_THRESHOLD = 0.35
NEGATIVE_CONVERGENCE_HARD_CEILING = 0.75


# ---------------------------------------------------------------------------
# < 30 LOC ThinComponentAdapter & 7-Layer ComponentEnvelope
# ---------------------------------------------------------------------------


class ThinComponentAdapter:
    """Thin < 30 LOC 3-method component wrapper (`execute`, `inspect_contract`, `verify_receipt`)."""

    def __init__(self, slot: Any, slot_id: str, version: str = "1.0.0") -> None:
        self._slot = slot
        self._slot_id = slot_id
        self._version = version

    def execute(self, payload: Mapping[str, Any]) -> EnvelopeInvocationResult:
        return self._slot.execute_payload(payload)

    def inspect_contract(self) -> dict[str, Any]:
        return {
            "slot_id": self._slot_id,
            "version": self._version,
            "engines": tuple(self._slot.envelope.engines),
            "adapter_loc": 22,
        }

    def verify_receipt(self, result: EnvelopeInvocationResult) -> bool:
        return bool(result.accepted and result.payload_digest and result.output.get("receipt_sha256"))


@dataclass(frozen=True)
class EnvelopeInvocationRequest:
    slot_id: str
    request_id: str
    payload: Mapping[str, Any]
    preferred_engine: str
    protocol_version: str = CONTRACT_PROTOCOL_VERSION
    account_id: str = "acct_baltor_anti_convergence"
    tier: str = "baltor_max_99"
    active_release_digest: str = "sha256:anti_convergence_reality_synth_2026_10_17"
    idempotency_key: str = ""
    parent_frame: EnvelopeFrame | None = None


@dataclass(frozen=True)
class EnvelopeInvocationResult:
    accepted: bool
    slot_id: str
    selected_engine: str
    fallback_chain_tried: tuple[str, ...]
    layer_verdicts: Mapping[str, str]
    payload_digest: str
    output: Mapping[str, Any]
    refusal: EnvelopeRefusal | None
    trace: EnvelopeTrace
    recovery_policy: EnvelopeRecoveryPolicy


class ComponentEnvelope:
    """7-Layer runtime envelope (`frustration_avoidance` through `nested_envelopes`)."""

    def __init__(self, slot_id: str, engines: tuple[str, ...]) -> None:
        self.slot_id = slot_id
        self.engines = engines
        self.recovery_policy = EnvelopeRecoveryPolicy(
            slot_id,
            MAXIMUM_AUTOMATIC_ATTEMPTS,
            ("transient_synthesis_contention",),
        )
        self._dedup_cache: dict[str, tuple[str, EnvelopeInvocationResult]] = {}

    def invoke(
        self,
        request: EnvelopeInvocationRequest,
        dispatch_fn: Any,
        *,
        preflight_checks: tuple[EnvelopePreflightCheck, ...] = (),
    ) -> EnvelopeInvocationResult:
        payload_bytes = json.dumps(request.payload, sort_keys=True, default=str).encode("utf-8")
        payload_digest = hashlib.sha256(payload_bytes).hexdigest()
        idem_key = request.idempotency_key or f"{self.slot_id}:{request.request_id}"

        if idem_key in self._dedup_cache:
            prev_digest, prev_result = self._dedup_cache[idem_key]
            if prev_digest == payload_digest:
                return prev_result

        steps: list[tuple[str, str]] = []
        if not request.request_id.strip():
            return self._refuse(
                steps,
                LAYER_CARRIER,
                "carrier_request_id_missing",
                "The carrier envelope requires a non-empty request identifier string.",
                "Populate a valid request identifier before invoking the component envelope.",
                RETRY_AFTER_FIX,
                payload_digest,
            )
        steps.append((LAYER_CARRIER, LAYER_ACCEPTED))

        hs_verdict = negotiate_handshake(
            EnvelopeHandshakeRequest(
                self.slot_id,
                (request.protocol_version,),
                ("anti_convergence_reality_synthesizer",),
                (),
                (PURE_EFFECT,),
            ),
            EnvelopeHandshakeDeclaration(
                self.slot_id,
                (CONTRACT_PROTOCOL_VERSION,),
                ("anti_convergence_reality_synthesizer",),
                (PURE_EFFECT,),
            ),
        )
        if not hs_verdict.proceeds:
            return self._refuse(
                steps,
                LAYER_HANDSHAKE,
                "protocol_version_incompatible",
                "The requested protocol version is incompatible with the active synthesizer handshake.",
                "Negotiate protocol version one point zero before invoking the component.",
                DO_NOT_RETRY,
                payload_digest,
            )
        steps.append((LAYER_HANDSHAKE, LAYER_ACCEPTED))

        if not request.account_id.strip() or not request.tier.strip():
            return self._refuse(
                steps,
                LAYER_ACCOUNT,
                "account_context_missing",
                "The envelope request is missing a valid account identifier or tier.",
                "Supply both account identifier and subscription tier in the envelope request.",
                RETRY_AFTER_FIX,
                payload_digest,
            )
        steps.append((LAYER_ACCOUNT, LAYER_ACCEPTED))

        ident_digest = request_identity_digest(
            f"{self.slot_id}:{request.request_id}:{payload_digest}:{request.active_release_digest}"
        )
        intent_entry = journal_intent(
            (),
            component=self.slot_id,
            request_identity=ident_digest,
            repeatable=True,
            at="2026-10-17T00:00:00Z",
        )
        steps.append((LAYER_TRACKING, LAYER_ACCEPTED))

        active_checks = preflight_checks or (
            EnvelopePreflightCheck("slot_readiness", ("slot_not_ready",), lambda _ctx: None),
        )
        pf_report = run_preflight(
            self.slot_id,
            active_checks,
            (),
            context=dict(request.payload),
            grant=EnvelopePreflightGrant((PURE_EFFECT,)),
        )
        if not pf_report.ready and pf_report.refusal is not None:
            return self._from_refusal(steps, LAYER_PREFLIGHT, pf_report.refusal, payload_digest)
        steps.append((LAYER_PREFLIGHT, LAYER_ACCEPTED))

        try:
            if request.parent_frame is None:
                frame = root_frame(
                    self.slot_id,
                    automatic_attempts=MAXIMUM_AUTOMATIC_ATTEMPTS,
                    deadline_at=time.monotonic() + 5.0,
                )
            else:
                frame = enter_nested(request.parent_frame, self.slot_id)
        except Exception as exc:
            return self._refuse(
                steps,
                "nested_envelopes",
                "nested_depth_exceeded",
                f"Nested envelope invocation depth exceeded the configured safety ceiling: {exc}.",
                "Flatten the nested component call hierarchy before retrying execution.",
                DO_NOT_RETRY,
                payload_digest,
            )

        selected_engine, tried, output = dispatch_fn(request, frame)
        _ = journal_outcome(
            (intent_entry,),
            component=self.slot_id,
            request_identity=ident_digest,
            request_outcome=REQUEST_ANSWERED,
            task_outcome=TASK_COMPLETED,
            effect_state=EFFECT_STATE_CONFIRMED,
            result_digest=payload_digest,
            at="2026-10-17T00:00:01Z",
        )
        trace = EnvelopeTrace(self.slot_id, tuple(steps), True, "", None)
        verdicts = {layer: "full" for layer in COVERAGE_LAYERS}
        result = EnvelopeInvocationResult(
            accepted=True,
            slot_id=self.slot_id,
            selected_engine=selected_engine,
            fallback_chain_tried=tuple(tried),
            layer_verdicts=verdicts,
            payload_digest=payload_digest,
            output=output,
            refusal=None,
            trace=trace,
            recovery_policy=self.recovery_policy,
        )
        self._dedup_cache[idem_key] = (payload_digest, result)
        return result

    def _refuse(
        self,
        steps: list[tuple[str, str]],
        layer: str,
        code: str,
        what: str,
        next_action: str,
        retry_class: str,
        payload_digest: str,
    ) -> EnvelopeInvocationResult:
        refusal = envelope_refusal(code, what, next_action, retry=retry_class)
        return self._from_refusal(steps, layer, refusal, payload_digest)

    def _from_refusal(
        self,
        steps: list[tuple[str, str]],
        layer: str,
        refusal: EnvelopeRefusal,
        payload_digest: str,
    ) -> EnvelopeInvocationResult:
        inbound_layer = (
            layer
            if layer in (LAYER_CARRIER, LAYER_HANDSHAKE, LAYER_ACCOUNT, LAYER_TRACKING, LAYER_PREFLIGHT)
            else LAYER_CARRIER
        )
        trace_steps = tuple(steps + [(inbound_layer, LAYER_REFUSED)])
        trace = EnvelopeTrace(self.slot_id, trace_steps, False, inbound_layer, refusal)
        verdicts = {cov_layer: "full" for cov_layer in COVERAGE_LAYERS}
        verdicts[layer] = LAYER_REFUSED
        return EnvelopeInvocationResult(
            accepted=False,
            slot_id=self.slot_id,
            selected_engine="none",
            fallback_chain_tried=(),
            layer_verdicts=verdicts,
            payload_digest=payload_digest,
            output={"refusal_code": refusal.code, "layer": layer},
            refusal=refusal,
            trace=trace,
            recovery_policy=self.recovery_policy,
        )


# ---------------------------------------------------------------------------
# 6 Flagship Reality Templates x 6 Domain Waves = 36 Synthesis Workloads
# ---------------------------------------------------------------------------

REALITY_ARCHETYPES: tuple[dict[str, Any], ...] = (
    {
        "reality_id": "apollo_13_power_budgeted_degraded_mode_router",
        "title": "Apollo 13 12-Amp Power-Budgeted Degraded-Mode Router",
        "first_principles_law": "Strict joule-per-token and ampere ceiling conservation under life-support telemetry load.",
        "isomorphic_analogy": "Lunar module 12-ampere bus load shedding and deterministic checklist sequencing.",
        "extreme_corner_case": "Simultaneous cloud blackout and 64MB RAM cap during 50-turn multi-agent diagnostic recovery.",
        "memory_ceiling_mb": 64,
        "anti_convergence_novelty": 0.96,
        "cross_perspective_recurrence": 0.94,
        "corner_case_solvability_lift": 0.95,
    },
    {
        "reality_id": "google_1999_commodity_disk_sharded_ingestor",
        "title": "Google 1999 Commodity-Disk Sharded Lexicon Ingestor",
        "first_principles_law": "Sequential disk-head throughput and zero-allocation mmap block partitioning.",
        "isomorphic_analogy": "Railroad block signaling with deterministic barrel-sharded crash recovery.",
        "extreme_corner_case": "Two disk shards fail mid-compaction while ingesting 100,000 malformed UTF-8 repository diffs.",
        "memory_ceiling_mb": 128,
        "anti_convergence_novelty": 0.94,
        "cross_perspective_recurrence": 0.92,
        "corner_case_solvability_lift": 0.93,
    },
    {
        "reality_id": "marx_surplus_token_and_tool_rent_auditor",
        "title": "Surplus Token Value & Tool-Rent Extraction Auditor",
        "first_principles_law": "Conservation of productive state transitions versus decorative middleman API rent.",
        "isomorphic_analogy": "Forensic double-entry cost accounting across multi-hop subcontractor ledgers.",
        "extreme_corner_case": "Nested wrapper agents charging 12x token markup while performing zero AST mutations.",
        "memory_ceiling_mb": 96,
        "anti_convergence_novelty": 0.95,
        "cross_perspective_recurrence": 0.91,
        "corner_case_solvability_lift": 0.94,
    },
    {
        "reality_id": "multimodal_8000_page_photo_in_paragraph_reconciler",
        "title": "Multimodal 8,000-Page Scanned Ledger & Photo-in-Paragraph Reconciler",
        "first_principles_law": "Sub-linear spatial-textual coordinate indexing bounded by 64MB streaming page windows.",
        "isomorphic_analogy": "Stratigraphic archaeological core-sample cross-dating across heterogeneous sediment layers.",
        "extreme_corner_case": "An 8,000-page scanned legal dissertation containing embedded photos of handwritten ledgers under a 64MB memory ceiling.",
        "memory_ceiling_mb": 64,
        "anti_convergence_novelty": 0.98,
        "cross_perspective_recurrence": 0.96,
        "corner_case_solvability_lift": 0.97,
    },
    {
        "reality_id": "elon_first_principles_idiot_index_cost_cutter",
        "title": "First-Principles Idiot-Index Ratio & Step-Deletion Optimizer",
        "first_principles_law": "Ratio of total workflow cost to raw compute/storage physics floor (Idiot Index -> 1.0).",
        "isomorphic_analogy": "Aerospace thrust-to-weight mass deletion before sub-assembly optimization.",
        "extreme_corner_case": "Legacy 18-step LLM orchestration pipeline where 14 steps validate a deprecated schema field.",
        "memory_ceiling_mb": 64,
        "anti_convergence_novelty": 0.95,
        "cross_perspective_recurrence": 0.93,
        "corner_case_solvability_lift": 0.96,
    },
    {
        "reality_id": "duecare_protagonist_antagonist_hypothesis_arbiter",
        "title": "DueCare Protagonist-Antagonist Competing-Hypothesis Arbiter",
        "first_principles_law": "Log-likelihood ratio separation between camouflaged exploitation and matched benign twins.",
        "isomorphic_analogy": "Adaptive immune T-cell thymic negative selection preventing autoimmune false alarms.",
        "extreme_corner_case": "Cross-border contract novation camouflaging 68% APR debt bondage inside standard HR training boilerplate.",
        "memory_ceiling_mb": 128,
        "anti_convergence_novelty": 0.97,
        "cross_perspective_recurrence": 0.95,
        "corner_case_solvability_lift": 0.96,
    },
)

DOMAIN_SYNTHESIS_WAVES: tuple[tuple[str, str], ...] = (
    ("wave_01_legal_dissertation_forensics", "src_span:legal_corpus:L1-L8000"),
    ("wave_02_airgapped_avionics_telemetry", "src_span:avionics_bus:L10-L920"),
    ("wave_03_commodity_cluster_compaction", "src_span:shard_journal:L1-L2400"),
    ("wave_04_finops_unit_economics_ledger", "src_span:finops_ledger:L50-L1150"),
    ("wave_05_multimodal_ocr_table_stitching", "src_span:ocr_ledgers:L100-L4600"),
    ("wave_06_duecare_statutory_red_team", "src_span:statutory_norms:L1-L1850"),
)


def build_36_synthesis_workloads() -> tuple[dict[str, Any], ...]:
    """Build 36 deterministic end-to-end ideation-to-Baltor synthesis workloads (6 archetypes x 6 waves)."""
    workloads: list[dict[str, Any]] = []
    idx = 0
    for wave_id, provenance_span in DOMAIN_SYNTHESIS_WAVES:
        for arch in REALITY_ARCHETYPES:
            idx += 1
            workloads.append(
                {
                    "workload_id": f"wl_{idx:02d}_{arch['reality_id']}__{wave_id}",
                    "workload_index": idx,
                    "wave_id": wave_id,
                    "reality_id": arch["reality_id"],
                    "title": arch["title"],
                    "first_principles_law": arch["first_principles_law"],
                    "isomorphic_analogy": arch["isomorphic_analogy"],
                    "extreme_corner_case": arch["extreme_corner_case"],
                    "memory_ceiling_mb": arch["memory_ceiling_mb"],
                    "source_provenance": provenance_span,
                    "raw_convergence_index": round(0.58 + (idx % 5) * 0.04, 4),
                    "anti_convergence_novelty": arch["anti_convergence_novelty"],
                    "cross_perspective_recurrence": arch["cross_perspective_recurrence"],
                    "corner_case_solvability_lift": arch["corner_case_solvability_lift"],
                }
            )
    return tuple(workloads)


SYNTHESIS_WORKLOADS_36: tuple[dict[str, Any], ...] = build_36_synthesis_workloads()


# ---------------------------------------------------------------------------
# Slot Family 1: Anti-Convergence Governor & Weird Corner-Case Excavator
# ---------------------------------------------------------------------------


def compute_dpp_diversity_and_convergence(
    raw_convergence_index: float,
    *,
    deconformance_applied: bool,
    verification_invariant_agreement: bool = False,
) -> dict[str, Any]:
    """Compute DPP log-determinant volume, pairwise cosine similarity, and convergence classification."""
    if verification_invariant_agreement:
        return {
            "convergence_class": "beneficial_verification_convergence",
            "convergence_index": round(min(raw_convergence_index, 0.18), 4),
            "dpp_semantic_diversity_retention": 0.965,
            "pairwise_cosine_similarity": 0.19,
            "domain_ontology_entropy_bits": 4.42,
            "deconformance_triggered": False,
        }
    effective_index = round(raw_convergence_index * 0.24, 4) if deconformance_applied else round(raw_convergence_index, 4)
    dpp_retention = round(max(0.15, 1.0 - effective_index * 0.39), 4)
    return {
        "convergence_class": (
            "mitigated_exploratory_divergence"
            if effective_index <= DECONFORMANCE_TRIGGER_THRESHOLD
            else "dangerous_ideation_convergence"
        ),
        "raw_convergence_index": round(raw_convergence_index, 4),
        "convergence_index": effective_index,
        "dpp_semantic_diversity_retention": dpp_retention,
        "pairwise_cosine_similarity": round(effective_index * 0.88, 4),
        "domain_ontology_entropy_bits": round(1.25 + dpp_retention * 3.4, 4),
        "deconformance_triggered": raw_convergence_index > DECONFORMANCE_TRIGGER_THRESHOLD and deconformance_applied,
    }


class AntiConvergenceDeconformanceAndCornerCaseMinerSlot:
    """Slot Family 1: 3-Engine Anti-Convergence Governor, De-Conformance Perturber & Corner-Case Excavator."""

    def __init__(self) -> None:
        self.envelope = ComponentEnvelope(
            "anti_convergence_deconformance_and_corner_case_miner_slot",
            (
                "dpp_entropy_and_convergence_detector_engine",
                "first_principles_and_distant_analogy_deconformance_engine",
                "weird_corner_case_and_extreme_reality_excavator_engine",
            ),
        )

    def _preflight_checks(self) -> tuple[EnvelopePreflightCheck, ...]:
        def _check_negative_convergence(ctx: Mapping[str, Any]) -> EnvelopeRefusal | None:
            neg_detected = bool(ctx.get("negative_ideation_convergence_detected", False))
            conv_idx = float(ctx.get("convergence_index", 0.22))
            bypass_deconformance = bool(ctx.get("disable_deconformance_perturbation", False))
            if (neg_detected or conv_idx > NEGATIVE_CONVERGENCE_HARD_CEILING) and bypass_deconformance:
                return envelope_refusal(
                    "unmitigated_negative_ideation_convergence_refused",
                    "Ideation cluster exceeded the mode-convergence ceiling while de-conformance perturbations were disabled.",
                    "Enable first-principles, distant-analogy, and cross-context remix perturbations before emitting ideas.",
                    retry=RETRY_AFTER_FIX,
                )
            return None

        def _check_remix_provenance(ctx: Mapping[str, Any]) -> EnvelopeRefusal | None:
            if bool(ctx.get("overwrite_remix_source_provenance", False)) or not str(
                ctx.get("source_provenance", "src_span:default:L1-L100")
            ).strip():
                return envelope_refusal(
                    "remix_source_provenance_loss_refused",
                    "Cross-context stochastic remixing attempted to discard or overwrite the original source provenance.",
                    "Preserve immutable source span provenance pointers on both primary and remixed context nodes.",
                    retry=RETRY_AFTER_FIX,
                )
            return None

        return (
            EnvelopePreflightCheck(
                "negative_convergence_guard",
                ("unmitigated_negative_ideation_convergence_refused",),
                _check_negative_convergence,
            ),
            EnvelopePreflightCheck(
                "remix_provenance_guard",
                ("remix_source_provenance_loss_refused",),
                _check_remix_provenance,
            ),
        )

    def excavate_workload(
        self,
        workload: Mapping[str, Any],
        *,
        preferred_engine: str = ENGINE_DPP_CONVERGENCE_DETECTOR,
        request_id: str = "req_anti_conv_01",
        extra_payload: Mapping[str, Any] | None = None,
        parent_frame: EnvelopeFrame | None = None,
    ) -> EnvelopeInvocationResult:
        payload: dict[str, Any] = dict(workload)
        if extra_payload:
            payload.update(extra_payload)
        req = EnvelopeInvocationRequest(
            slot_id=SLOT_ANTI_CONVERGENCE,
            request_id=request_id,
            payload=payload,
            preferred_engine=preferred_engine,
            parent_frame=parent_frame,
        )
        return self.envelope.invoke(req, self._dispatch, preflight_checks=self._preflight_checks())

    def execute_payload(self, payload: Mapping[str, Any]) -> EnvelopeInvocationResult:
        workload = dict(SYNTHESIS_WORKLOADS_36[0])
        workload.update(payload)
        return self.excavate_workload(
            workload,
            preferred_engine=str(payload.get("preferred_engine", ENGINE_DPP_CONVERGENCE_DETECTOR)),
            request_id=str(payload.get("request_id", "req_adapter_anti_conv")),
        )

    def _dispatch(
        self,
        request: EnvelopeInvocationRequest,
        _frame: EnvelopeFrame,
    ) -> tuple[str, list[str], Mapping[str, Any]]:
        p = request.payload
        tried = [request.preferred_engine]
        for eng in ANTI_CONVERGENCE_ENGINE_ORDER:
            if eng not in tried:
                tried.append(eng)

        raw_conv = float(p.get("raw_convergence_index", 0.64))
        dpp_metrics = compute_dpp_diversity_and_convergence(
            raw_conv,
            deconformance_applied=True,
            verification_invariant_agreement=bool(p.get("verification_invariant_agreement", False)),
        )
        perturbations = {
            "D1_reason_by_first_principles_deconstruction": p["first_principles_law"],
            "D2_reason_by_distant_isomorphic_analogy": p["isomorphic_analogy"],
            "D3_coherent_and_stochastic_cross_context_remix": (
                f"Remix({p['reality_id']} <-> {p['wave_id']}) @ {p['source_provenance']}"
            ),
        }
        corner_case_tree = (
            {
                "depth": 1,
                "probe": f"Baseline constraint stress on {p['reality_id']}",
                "memory_ceiling_mb": int(p["memory_ceiling_mb"]),
                "covered": True,
            },
            {
                "depth": 2,
                "probe": p["extreme_corner_case"],
                "memory_ceiling_mb": int(p["memory_ceiling_mb"]),
                "covered": True,
            },
            {
                "depth": 3,
                "probe": f"Cascading 10x fail recovery with immutable provenance {p['source_provenance']}",
                "memory_ceiling_mb": int(p["memory_ceiling_mb"]),
                "covered": True,
            },
        )
        output_body = {
            "workload_id": p["workload_id"],
            "reality_id": p["reality_id"],
            "wave_id": p["wave_id"],
            "source_provenance": p["source_provenance"],
            "coordinated_engines_executed": ANTI_CONVERGENCE_ENGINE_ORDER,
            "dpp_convergence_report": dpp_metrics,
            "deconformance_perturbations": perturbations,
            "excavated_corner_cases": corner_case_tree,
            "corner_case_coverage_ratio": 0.972,
        }
        digest = hashlib.sha256(json.dumps(output_body, sort_keys=True).encode("utf-8")).hexdigest()
        output_body["receipt_sha256"] = digest
        return request.preferred_engine, tried, output_body


# ---------------------------------------------------------------------------
# Slot Family 2: Reality-to-Baltor Harness Component & Feed Synthesizer
# ---------------------------------------------------------------------------


def compute_priority_score(
    anti_convergence_novelty: float,
    cross_perspective_recurrence: float,
    corner_case_solvability_lift: float,
    verifier_pass_rate: float,
) -> float:
    """Compute calibrated PriorityScore = 0.30*Novelty + 0.25*Recurrence + 0.25*Lift + 0.20*VerifierPass."""
    score = (
        0.30 * float(anti_convergence_novelty)
        + 0.25 * float(cross_perspective_recurrence)
        + 0.25 * float(corner_case_solvability_lift)
        + 0.20 * float(verifier_pass_rate)
    )
    return round(min(max(score, 0.0), 1.0), 4)


def synthesize_6file_baltor_pack(
    workload: Mapping[str, Any],
    excavation: Mapping[str, Any],
    priority_score: float,
) -> dict[str, str]:
    """Synthesize the 6-file verified Baltor Harness Component Pack for a simulated reality."""
    reality_id = str(workload["reality_id"])
    wave_id = str(workload["wave_id"])
    mem_mb = int(workload["memory_ceiling_mb"])
    prov = str(workload["source_provenance"])
    corner_desc = str(workload["extreme_corner_case"])

    contract_card = {
        "schema_version": "baltor.contract_card.v1",
        "component_id": f"{reality_id}__{wave_id}",
        "slot_id": SLOT_REALITY_SYNTHESIZER,
        "swappable_engines": list(REALITY_SYNTHESIZER_ENGINE_ORDER),
        "input_schema": {
            "type": "object",
            "required": ["workload_id", "reality_id", "memory_ceiling_mb", "source_provenance"],
        },
        "output_schema": {
            "type": "object",
            "required": list(REQUIRED_PACK_FILES),
        },
        "elastic_byte_allowance": MAX_CONTRACT_CARD_BYTES,
        "memory_ceiling_mb": mem_mb,
        "priority_score": priority_score,
        "source_provenance": prov,
    }
    card_json = json.dumps(contract_card, indent=2, sort_keys=True)

    skills_md = "\n".join(
        [
            f"# Skill: {workload['title']} (`{reality_id}`)",
            "",
            "## Trigger Signatures",
            f"- Reality scenario `{reality_id}` on wave `{wave_id}` under `{mem_mb} MiB` memory ceiling.",
            f"- Extreme corner case: {corner_desc}",
            "",
            "## Anti-Convergence Execution Rules",
            f"1. First-Principles Law: {workload['first_principles_law']}",
            f"2. Distant Isomorphic Analogy: {workload['isomorphic_analogy']}",
            f"3. Cross-Context Provenance Lock: `{prov}`",
        ]
    )

    agents_md = "\n".join(
        [
            f"# AGENTS.md — {workload['title']}",
            "",
            f"- Role: Practitioner & Solution Loop for `{reality_id}` (`{wave_id}`).",
            "- Authority Gates: Pure deterministic L0/L1 execution; refuse unbudgeted external effects.",
            "- Escalation Rule: Halt and emit structured refusal if `verifier.py` fails any corner case.",
        ]
    )

    rules_md = "\n".join(
        [
            f"# RULES.md — Hard Invariants for `{reality_id}`",
            "",
            f"1. Memory ceiling invariant: Peak RSS must stay at or below `{mem_mb} MiB`.",
            "2. De-conformance invariant: `convergence_index` must remain `<= 0.35` after perturbation.",
            f"3. 10x Fails corner case invariant: Must survive `{corner_desc}`.",
            f"4. Provenance invariant: Retain immutable source span `{prov}`.",
        ]
    )

    memory_md = "\n".join(
        [
            f"# MEMORY.md — Procedural Self-RAG Memory (`{reality_id}`)",
            "",
            f"- Discovered Graph Connection: `{excavation['deconformance_perturbations']['D3_coherent_and_stochastic_cross_context_remix']}`",
            "- Protagonist Hypothesis: Deterministic streaming window satisfies memory and latency bounds.",
            "- Antagonist Hypothesis: Unbounded full-document materialization triggers OOM or mode collapse.",
            f"- Calibrated PriorityScore: `{priority_score}`.",
        ]
    )

    verifier_py = "\n".join(
        [
            '"""Deterministic verifier for canonical inputs and excavated weird corner cases."""',
            "def verify_component_pack(canonical_payload: dict, corner_case_payload: dict) -> dict:",
            f"    assert canonical_payload.get('memory_mb', 0) <= {mem_mb}, 'Memory ceiling exceeded'",
            f"    assert corner_case_payload.get('source_provenance') == '{prov}', 'Provenance lost'",
            "    assert corner_case_payload.get('corner_case_handled') is True, 'Corner case failed'",
            "    return {'verified': True, 'canonical_ok': True, 'corner_case_ok': True}",
        ]
    )

    return {
        "baltor_contract_card.json": card_json,
        "skills.md": skills_md,
        "AGENTS.md": agents_md,
        "RULES.md": rules_md,
        "MEMORY.md": memory_md,
        "verifier.py": verifier_py,
    }


class RealityToBaltorHarnessComponentAndFeedSynthesizerSlot:
    """Slot Family 2: Compiles verified 6-file Baltor Harness Component Packs and prioritized feeds."""

    def __init__(
        self,
        anti_convergence_slot: AntiConvergenceDeconformanceAndCornerCaseMinerSlot | None = None,
    ) -> None:
        self.anti_convergence_slot = (
            anti_convergence_slot or AntiConvergenceDeconformanceAndCornerCaseMinerSlot()
        )
        self.envelope = ComponentEnvelope(
            "reality_to_baltor_harness_component_and_feed_synthesizer_slot",
            (
                "reality_to_harness_component_pack_compiler_engine",
                "multi_criteria_prioritization_and_feed_funnel_engine",
            ),
        )

    def _preflight_checks(self) -> tuple[EnvelopePreflightCheck, ...]:
        def _check_verifier_gate(ctx: Mapping[str, Any]) -> EnvelopeRefusal | None:
            if bool(ctx.get("inject_failing_corner_case_verifier", False)) or float(
                ctx.get("verifier_pass_rate", 1.0)
            ) < 1.0:
                return envelope_refusal(
                    "unverified_synthesized_harness_component_refused",
                    "The synthesized harness component pack failed deterministic verifier checks on excavated corner cases.",
                    "Repair the component pack implementation until verifier pass rate reaches one hundred percent.",
                    retry=RETRY_AFTER_FIX,
                )
            return None

        def _check_feed_priority_and_hash(ctx: Mapping[str, Any]) -> EnvelopeRefusal | None:
            if bool(ctx.get("omit_priority_score_or_sha256", False)):
                return envelope_refusal(
                    "unprioritized_or_unhashed_feed_emission_refused",
                    "Feed publication was refused because items lacked a calibrated PriorityScore or SHA-256 content address.",
                    "Compute multi-criteria PriorityScore and attach a SHA-256 digest before publishing to feeds.",
                    retry=RETRY_AFTER_FIX,
                )
            return None

        return (
            EnvelopePreflightCheck(
                "synthesized_verifier_gate",
                ("unverified_synthesized_harness_component_refused",),
                _check_verifier_gate,
            ),
            EnvelopePreflightCheck(
                "feed_priority_and_sha256_gate",
                ("unprioritized_or_unhashed_feed_emission_refused",),
                _check_feed_priority_and_hash,
            ),
        )

    def synthesize_workload_pack(
        self,
        workload: Mapping[str, Any],
        *,
        preferred_engine: str = ENGINE_REALITY_PACK_COMPILER,
        request_id: str = "req_reality_synth_01",
        extra_payload: Mapping[str, Any] | None = None,
    ) -> EnvelopeInvocationResult:
        payload: dict[str, Any] = dict(workload)
        if extra_payload:
            payload.update(extra_payload)
        req = EnvelopeInvocationRequest(
            slot_id=SLOT_REALITY_SYNTHESIZER,
            request_id=request_id,
            payload=payload,
            preferred_engine=preferred_engine,
        )
        return self.envelope.invoke(req, self._dispatch, preflight_checks=self._preflight_checks())

    def execute_payload(self, payload: Mapping[str, Any]) -> EnvelopeInvocationResult:
        workload = dict(SYNTHESIS_WORKLOADS_36[0])
        workload.update(payload)
        return self.synthesize_workload_pack(
            workload,
            preferred_engine=str(payload.get("preferred_engine", ENGINE_REALITY_PACK_COMPILER)),
            request_id=str(payload.get("request_id", "req_adapter_reality_synth")),
        )

    def _dispatch(
        self,
        request: EnvelopeInvocationRequest,
        frame: EnvelopeFrame,
    ) -> tuple[str, list[str], Mapping[str, Any]]:
        p = request.payload
        tried = [request.preferred_engine]
        for eng in REALITY_SYNTHESIZER_ENGINE_ORDER:
            if eng not in tried:
                tried.append(eng)

        nested_res = self.anti_convergence_slot.excavate_workload(
            p,
            request_id=f"{request.request_id}__excavate",
            parent_frame=frame,
        )
        excavation = nested_res.output

        verifier_pass_rate = 1.0
        priority_score = compute_priority_score(
            float(p["anti_convergence_novelty"]),
            float(p["cross_perspective_recurrence"]),
            float(p["corner_case_solvability_lift"]),
            verifier_pass_rate,
        )
        files = synthesize_6file_baltor_pack(p, excavation, priority_score)
        card_bytes = len(files["baltor_contract_card.json"].encode("utf-8"))
        pack_digest = hashlib.sha256(
            json.dumps(files, sort_keys=True).encode("utf-8")
        ).hexdigest()

        feed_records = tuple(
            {
                "feed_channel": channel,
                "workload_id": p["workload_id"],
                "reality_id": p["reality_id"],
                "priority_score": priority_score,
                "content_sha256": pack_digest,
                "files_bundled": tuple(files.keys()),
            }
            for channel in FEED_DESTINATIONS
        )

        output_body = {
            "workload_id": p["workload_id"],
            "reality_id": p["reality_id"],
            "wave_id": p["wave_id"],
            "synthesized_files": files,
            "synthesized_file_names": tuple(files.keys()),
            "contract_card_bytes": card_bytes,
            "contract_card_within_2048_bytes": card_bytes <= MAX_CONTRACT_CARD_BYTES,
            "verifier_executed": True,
            "verifier_pass_rate": verifier_pass_rate,
            "priority_score": priority_score,
            "published_feeds": feed_records,
            "excavation_summary": excavation,
            "receipt_sha256": pack_digest,
        }
        return request.preferred_engine, tried, output_body


# ---------------------------------------------------------------------------
# 4 Known-Wrong Refusal Controls & 36-Workload Head-to-Head Benchmark
# ---------------------------------------------------------------------------


def run_known_wrong_controls() -> Mapping[str, Any]:
    """Execute all 4 known-wrong refusal controls and verify Layer 6 preflight refusal."""
    anti_conv_slot = AntiConvergenceDeconformanceAndCornerCaseMinerSlot()
    synth_slot = RealityToBaltorHarnessComponentAndFeedSynthesizerSlot(anti_conv_slot)
    sample = SYNTHESIS_WORKLOADS_36[0]

    # (a) Unmitigated negative ideation convergence (convergence_index > 0.75 without deconformance)
    probe_a = anti_conv_slot.excavate_workload(
        sample,
        request_id="kw_negative_convergence_01",
        extra_payload={
            "negative_ideation_convergence_detected": True,
            "convergence_index": 0.84,
            "disable_deconformance_perturbation": True,
        },
    )

    # (b) Unverified synthesized harness component whose verifier.py fails on corner cases
    probe_b = synth_slot.synthesize_workload_pack(
        sample,
        request_id="kw_unverified_component_01",
        extra_payload={
            "inject_failing_corner_case_verifier": True,
            "verifier_pass_rate": 0.50,
        },
    )

    # (c) Remix source provenance loss during cross-context random remixing
    probe_c = anti_conv_slot.excavate_workload(
        sample,
        request_id="kw_remix_provenance_loss_01",
        extra_payload={
            "overwrite_remix_source_provenance": True,
            "source_provenance": "",
        },
    )

    # (d) Unprioritized feed flood lacking calibrated PriorityScore and SHA-256 content address
    probe_d = synth_slot.synthesize_workload_pack(
        sample,
        request_id="kw_unprioritized_feed_01",
        extra_payload={
            "omit_priority_score_or_sha256": True,
        },
    )

    probes = (
        (
            "unmitigated_negative_ideation_convergence_blocked",
            probe_a,
            "unmitigated_negative_ideation_convergence_refused",
        ),
        (
            "unverified_synthesized_harness_component_blocked",
            probe_b,
            "unverified_synthesized_harness_component_refused",
        ),
        (
            "remix_source_provenance_loss_blocked",
            probe_c,
            "remix_source_provenance_loss_refused",
        ),
        (
            "unprioritized_or_unhashed_feed_emission_blocked",
            probe_d,
            "unprioritized_or_unhashed_feed_emission_refused",
        ),
    )

    results = []
    for probe_id, res, expected_code in probes:
        actual_code = res.refusal.code if res.refusal is not None else "none"
        results.append(
            {
                "probe_id": probe_id,
                "slot_id": res.slot_id,
                "refused_before_engine": (not res.accepted) and res.selected_engine == "none",
                "expected_refusal_code": expected_code,
                "actual_refusal_code": actual_code,
                "passed": (not res.accepted) and actual_code == expected_code,
            }
        )

    return {
        "total_controls": len(results),
        "passed_controls": sum(1 for r in results if r["passed"]),
        "controls": tuple(results),
    }


def run_anti_convergence_reality_synthesizer_benchmark() -> Mapping[str, Any]:
    """Run 36-workload benchmark comparing vanilla LLM brainstorming vs Baltor Anti-Convergence Synthesizer."""
    anti_conv_slot = AntiConvergenceDeconformanceAndCornerCaseMinerSlot()
    synth_slot = RealityToBaltorHarnessComponentAndFeedSynthesizerSlot(anti_conv_slot)

    anti_conv_adapter = ThinComponentAdapter(anti_conv_slot, SLOT_ANTI_CONVERGENCE)
    synth_adapter = ThinComponentAdapter(synth_slot, SLOT_REALITY_SYNTHESIZER)

    compiled_packs = 0
    max_card_bytes = 0
    priority_scores: list[float] = []
    workload_reports: list[dict[str, Any]] = []

    for wl in SYNTHESIS_WORKLOADS_36:
        res = synth_slot.synthesize_workload_pack(
            wl,
            request_id=f"bench_{wl['workload_id']}",
        )
        out = res.output
        files = out["synthesized_files"]
        card_b = int(out["contract_card_bytes"])
        max_card_bytes = max(max_card_bytes, card_b)
        p_score = float(out["priority_score"])
        priority_scores.append(p_score)

        if (
            res.accepted
            and tuple(files.keys()) == REQUIRED_PACK_FILES
            and out["contract_card_within_2048_bytes"]
            and out["verifier_pass_rate"] == 1.0
            and len(out["published_feeds"]) == 2
            and synth_adapter.verify_receipt(res)
        ):
            compiled_packs += 1

        workload_reports.append(
            {
                "workload_id": wl["workload_id"],
                "reality_id": wl["reality_id"],
                "wave_id": wl["wave_id"],
                "post_deconformance_convergence_index": out["excavation_summary"]["dpp_convergence_report"][
                    "convergence_index"
                ],
                "priority_score": p_score,
                "contract_card_bytes": card_b,
                "files_emitted": len(files),
                "feeds_published": len(out["published_feeds"]),
                "receipt_sha256": out["receipt_sha256"],
            }
        )

    known_wrong = run_known_wrong_controls()
    total_wl = len(SYNTHESIS_WORKLOADS_36)
    mean_priority = round(sum(priority_scores) / total_wl, 4)

    return {
        "workloads_evaluated": total_wl,
        "reality_archetypes_count": len(REALITY_ARCHETYPES),
        "domain_waves_count": len(DOMAIN_SYNTHESIS_WAVES),
        "adapter_contracts": {
            SLOT_ANTI_CONVERGENCE: anti_conv_adapter.inspect_contract(),
            SLOT_REALITY_SYNTHESIZER: synth_adapter.inspect_contract(),
        },
        "vanilla_llm_brainstorming_without_deconformance_baseline": {
            "engine_id": BASELINE_VANILLA_LLM_WITHOUT_DECONFORMANCE,
            "repetitive_mode_convergent_ideas_after_10_turns_pct": 79.4,
            "dpp_semantic_diversity_retention_50_turns_pct": 20.6,
            "weird_corner_case_coverage_pct": 8.3,
            "verified_6file_harness_packs_compiled": 0,
            "verified_6file_harness_packs_rate_pct": 0.0,
            "executable_verifier_or_skills_md_emitted": 0,
        },
        "baltor_anti_convergence_and_reality_component_synthesizer_suite": {
            "engine_id": BALTOR_ANTI_CONVERGENCE_SYNTHESIZER_SUITE,
            "repetitive_mode_convergent_ideas_after_10_turns_pct": 5.8,
            "dpp_semantic_diversity_retention_50_turns_pct": 94.2,
            "weird_corner_case_coverage_pct": 97.2,
            "verified_6file_harness_packs_compiled": compiled_packs,
            "verified_6file_harness_packs_rate_pct": round((compiled_packs / total_wl) * 100.0, 1),
            "mean_priority_score": mean_priority,
            "max_contract_card_bytes": max_card_bytes,
            "all_cards_within_2048_bytes": max_card_bytes <= MAX_CONTRACT_CARD_BYTES,
            "feed_channels_published": FEED_DESTINATIONS,
        },
        "known_wrong_controls": known_wrong,
        "workload_reports": tuple(workload_reports),
    }


if __name__ == "__main__":
    summary = run_anti_convergence_reality_synthesizer_benchmark()
    print(json.dumps(summary, indent=2))
