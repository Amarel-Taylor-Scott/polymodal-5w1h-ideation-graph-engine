"""Unit tests for the Anti-Convergence / De-Conformance Governor & Automated Reality-to-Baltor.ai
Harness Component (`skills.md`, `AGENTS.md`, `RULES.md`, `MEMORY.md`, `baltor_contract_card.json`,
`verifier.py`, and `agentfeeds.si` Feeds) Synthesizer Engine Suite.
"""
from __future__ import annotations

import inspect
import json
from pathlib import Path
import sys
import unittest

REPOSITORY = Path(__file__).resolve().parents[1]
if str(REPOSITORY / "src") not in sys.path:
    sys.path.insert(0, str(REPOSITORY / "src"))
if str(REPOSITORY / "tools") not in sys.path:
    sys.path.insert(0, str(REPOSITORY / "tools"))

from anti_convergence_reality_to_baltor_component_synthesizer_engines import (  # noqa: E402
    ANTI_CONVERGENCE_ENGINE_ORDER,
    BALTOR_ANTI_CONVERGENCE_SYNTHESIZER_SUITE,
    BASELINE_VANILLA_LLM_WITHOUT_DECONFORMANCE,
    DECONFORMANCE_PERTURBATION_MODES,
    FEED_DESTINATIONS,
    MAX_CONTRACT_CARD_BYTES,
    REALITY_ARCHETYPES,
    REALITY_SYNTHESIZER_ENGINE_ORDER,
    REQUIRED_PACK_FILES,
    SLOT_ANTI_CONVERGENCE,
    SLOT_REALITY_SYNTHESIZER,
    SYNTHESIS_WORKLOADS_36,
    AntiConvergenceDeconformanceAndCornerCaseMinerSlot,
    EnvelopeInvocationRequest,
    RealityToBaltorHarnessComponentAndFeedSynthesizerSlot,
    ThinComponentAdapter,
    compute_dpp_diversity_and_convergence,
    compute_priority_score,
    run_anti_convergence_reality_synthesizer_benchmark,
    run_known_wrong_controls,
)


class AntiConvergenceRealityToBaltorSynthesizerTests(unittest.TestCase):
    """Verify Slot Family 1, Slot Family 2, ThinComponentAdapter, 36 workloads, and 4 known-wrong controls."""

    def test_thin_component_adapter_loc_and_contract(self) -> None:
        source_lines = [
            line
            for line in inspect.getsourcelines(ThinComponentAdapter)[0]
            if line.strip() and not line.strip().startswith("#")
        ]
        self.assertLess(len(source_lines), 30)

        slot_1 = AntiConvergenceDeconformanceAndCornerCaseMinerSlot()
        slot_2 = RealityToBaltorHarnessComponentAndFeedSynthesizerSlot(slot_1)
        adapter_1 = ThinComponentAdapter(slot_1, SLOT_ANTI_CONVERGENCE)
        adapter_2 = ThinComponentAdapter(slot_2, SLOT_REALITY_SYNTHESIZER)

        c1 = adapter_1.inspect_contract()
        c2 = adapter_2.inspect_contract()
        self.assertEqual(c1["slot_id"], SLOT_ANTI_CONVERGENCE)
        self.assertEqual(c1["engines"], ANTI_CONVERGENCE_ENGINE_ORDER)
        self.assertEqual(c2["slot_id"], SLOT_REALITY_SYNTHESIZER)
        self.assertEqual(c2["engines"], REALITY_SYNTHESIZER_ENGINE_ORDER)

        r1 = adapter_1.execute({"request_id": "test_adapter_1"})
        r2 = adapter_2.execute({"request_id": "test_adapter_2"})
        self.assertTrue(adapter_1.verify_receipt(r1))
        self.assertTrue(adapter_2.verify_receipt(r2))

    def test_beneficial_vs_dangerous_convergence_and_deconformance_triggers(self) -> None:
        # Beneficial verification convergence is preserved without perturbation
        beneficial = compute_dpp_diversity_and_convergence(
            0.82,
            deconformance_applied=False,
            verification_invariant_agreement=True,
        )
        self.assertEqual(beneficial["convergence_class"], "beneficial_verification_convergence")
        self.assertLessEqual(beneficial["convergence_index"], 0.35)
        self.assertFalse(beneficial["deconformance_triggered"])

        # Dangerous ideation convergence (> 0.35) triggers D1/D2/D3 de-conformance perturbations
        unmitigated = compute_dpp_diversity_and_convergence(0.68, deconformance_applied=False)
        self.assertEqual(unmitigated["convergence_class"], "dangerous_ideation_convergence")
        self.assertGreater(unmitigated["convergence_index"], 0.35)

        mitigated = compute_dpp_diversity_and_convergence(0.68, deconformance_applied=True)
        self.assertEqual(mitigated["convergence_class"], "mitigated_exploratory_divergence")
        self.assertLessEqual(mitigated["convergence_index"], 0.35)
        self.assertTrue(mitigated["deconformance_triggered"])

        slot_1 = AntiConvergenceDeconformanceAndCornerCaseMinerSlot()
        res = slot_1.excavate_workload(SYNTHESIS_WORKLOADS_36[3], request_id="test_8000_page_ledger")
        self.assertTrue(res.accepted)
        out = res.output
        self.assertEqual(tuple(out["deconformance_perturbations"].keys()), DECONFORMANCE_PERTURBATION_MODES)
        self.assertEqual(len(out["excavated_corner_cases"]), 3)
        self.assertIn("8,000-page scanned legal dissertation", out["excavated_corner_cases"][1]["probe"])

    def test_six_file_baltor_component_pack_and_priority_score_formula(self) -> None:
        expected_score = compute_priority_score(0.98, 0.96, 0.97, 1.0)
        self.assertAlmostEqual(expected_score, 0.30 * 0.98 + 0.25 * 0.96 + 0.25 * 0.97 + 0.20 * 1.0, places=4)

        reality_ids = tuple(a["reality_id"] for a in REALITY_ARCHETYPES)
        self.assertEqual(
            reality_ids,
            (
                "apollo_13_power_budgeted_degraded_mode_router",
                "google_1999_commodity_disk_sharded_ingestor",
                "marx_surplus_token_and_tool_rent_auditor",
                "multimodal_8000_page_photo_in_paragraph_reconciler",
                "elon_first_principles_idiot_index_cost_cutter",
                "duecare_protagonist_antagonist_hypothesis_arbiter",
            ),
        )

        synth_slot = RealityToBaltorHarnessComponentAndFeedSynthesizerSlot()
        res = synth_slot.synthesize_workload_pack(SYNTHESIS_WORKLOADS_36[0], request_id="test_pack_01")
        self.assertTrue(res.accepted)
        files = res.output["synthesized_files"]
        self.assertEqual(tuple(files.keys()), REQUIRED_PACK_FILES)
        self.assertLessEqual(res.output["contract_card_bytes"], MAX_CONTRACT_CARD_BYTES)

        card = json.loads(files["baltor_contract_card.json"])
        self.assertEqual(card["slot_id"], SLOT_REALITY_SYNTHESIZER)
        self.assertEqual(card["elastic_byte_allowance"], MAX_CONTRACT_CARD_BYTES)

        # Execute the generated verifier.py script deterministically
        ns: dict[str, object] = {}
        exec(files["verifier.py"], ns)  # noqa: S102
        verify_fn = ns["verify_component_pack"]
        verdict = verify_fn(  # type: ignore[operator]
            {"memory_mb": 32},
            {"source_provenance": SYNTHESIS_WORKLOADS_36[0]["source_provenance"], "corner_case_handled": True},
        )
        self.assertTrue(verdict["verified"])

        feeds = res.output["published_feeds"]
        self.assertEqual(tuple(f["feed_channel"] for f in feeds), FEED_DESTINATIONS)

    def test_four_known_wrong_refusal_controls(self) -> None:
        kw = run_known_wrong_controls()
        self.assertEqual(kw["total_controls"], 4)
        self.assertEqual(kw["passed_controls"], 4)
        expected_codes = (
            "unmitigated_negative_ideation_convergence_refused",
            "unverified_synthesized_harness_component_refused",
            "remix_source_provenance_loss_refused",
            "unprioritized_or_unhashed_feed_emission_refused",
        )
        for ctrl, exp_code in zip(kw["controls"], expected_codes):
            self.assertTrue(ctrl["passed"])
            self.assertTrue(ctrl["refused_before_engine"])
            self.assertEqual(ctrl["actual_refusal_code"], exp_code)

    def test_carrier_handshake_and_account_envelope_guards(self) -> None:
        slot = AntiConvergenceDeconformanceAndCornerCaseMinerSlot()
        bad_carrier = slot.envelope.invoke(
            EnvelopeInvocationRequest(
                slot_id=SLOT_ANTI_CONVERGENCE,
                request_id="   ",
                payload={"workload_id": "wl_bad"},
                preferred_engine=ANTI_CONVERGENCE_ENGINE_ORDER[0],
            ),
            slot._dispatch,
        )
        self.assertFalse(bad_carrier.accepted)
        self.assertEqual(bad_carrier.refusal.code, "carrier_request_id_missing")

        bad_hs = slot.envelope.invoke(
            EnvelopeInvocationRequest(
                slot_id=SLOT_ANTI_CONVERGENCE,
                request_id="req_bad_hs",
                payload={"workload_id": "wl_bad"},
                preferred_engine=ANTI_CONVERGENCE_ENGINE_ORDER[0],
                protocol_version="9.9",
            ),
            slot._dispatch,
        )
        self.assertFalse(bad_hs.accepted)
        self.assertEqual(bad_hs.refusal.code, "protocol_version_incompatible")

    def test_36_workload_end_to_end_benchmark(self) -> None:
        report = run_anti_convergence_reality_synthesizer_benchmark()
        self.assertEqual(report["workloads_evaluated"], 36)

        base = report["vanilla_llm_brainstorming_without_deconformance_baseline"]
        self.assertEqual(base["engine_id"], BASELINE_VANILLA_LLM_WITHOUT_DECONFORMANCE)
        self.assertEqual(base["repetitive_mode_convergent_ideas_after_10_turns_pct"], 79.4)
        self.assertEqual(base["weird_corner_case_coverage_pct"], 8.3)
        self.assertEqual(base["executable_verifier_or_skills_md_emitted"], 0)

        baltor = report["baltor_anti_convergence_and_reality_component_synthesizer_suite"]
        self.assertEqual(baltor["engine_id"], BALTOR_ANTI_CONVERGENCE_SYNTHESIZER_SUITE)
        self.assertEqual(baltor["dpp_semantic_diversity_retention_50_turns_pct"], 94.2)
        self.assertEqual(baltor["weird_corner_case_coverage_pct"], 97.2)
        self.assertEqual(baltor["verified_6file_harness_packs_compiled"], 36)
        self.assertEqual(baltor["verified_6file_harness_packs_rate_pct"], 100.0)
        self.assertTrue(baltor["all_cards_within_2048_bytes"])


if __name__ == "__main__":
    unittest.main()
