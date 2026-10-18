"""Unit and conformance tests for the Adversarial Perspective Prism, Famous Thinker /
Historical-Reality Simulator, and 10-Way Dialectical Challenge Engine Suite.
"""
from __future__ import annotations

from pathlib import Path
import sys
import unittest

REPOSITORY = Path(__file__).resolve().parents[1]
if str(REPOSITORY / "src") not in sys.path:
    sys.path.insert(0, str(REPOSITORY / "src"))
if str(REPOSITORY / "tools") not in sys.path:
    sys.path.insert(0, str(REPOSITORY / "tools"))

from perspective_prism_thinker_personas_and_10x_challenge_engines import (  # noqa: E402
    ALL_SLOTS,
    BALTOR_PERSPECTIVE_PRISM_AND_10X_SUITE,
    BASELINE_SINGLE_PERSONA_PARAPHRASE,
    DIALECTICAL_ENGINE_ORDER,
    DIALECTICAL_QUADRANTS_4,
    ENGINE_DETERMINISTIC_10X_FALLBACK,
    ENGINE_DETERMINISTIC_TRIAD_FALLBACK,
    ENGINE_HISTORICAL_REALITY_SIMULATOR,
    ENGINE_OPERATING_ENVELOPE_STRESS_MATRIX,
    HISTORICAL_CONSTRAINED_REALITIES_6,
    REPHRASER_ENGINE_ORDER,
    SLOT_DIALECTICAL_10X_CHALLENGER,
    SLOT_THINKER_AND_REALITY_REPHRASER,
    THINKER_PERSONAS_6,
    Dialectical10xWrongRightWorksFailsChallengerSlot,
    ThinkerPersonaAndHistoricalRealityRephraserSlot,
    ThinComponentAdapter,
    build_36_perspective_challenge_workloads,
    run_known_wrong_controls,
    run_perspective_prism_and_10x_benchmark,
)


class PerspectivePrismThinkerPersonasAnd10xChallengeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.rephraser = ThinkerPersonaAndHistoricalRealityRephraserSlot()
        self.challenger = Dialectical10xWrongRightWorksFailsChallengerSlot(self.rephraser)

    def test_slot_and_persona_reality_catalog_completeness(self) -> None:
        self.assertEqual(
            ALL_SLOTS,
            (
                "thinker_persona_and_historical_reality_rephraser_slot",
                "dialectical_10x_wrong_right_works_fails_challenger_slot",
            ),
        )
        self.assertEqual(len(THINKER_PERSONAS_6), 6)
        self.assertEqual(len(HISTORICAL_CONSTRAINED_REALITIES_6), 6)

        persona_ids = tuple(p["persona_id"] for p in THINKER_PERSONAS_6)
        self.assertEqual(
            persona_ids,
            (
                "P01_frontier_ai_researcher_scaling_and_causality",
                "P02_karl_marx_historical_materialist_critique",
                "P03_claude_shannon_information_entropy_channel",
                "P04_richard_feynman_first_principles_and_counterexample",
                "P05_judea_pearl_causal_do_calculus_investigator",
                "P06_adversarial_red_team_and_skeptical_auditor",
            ),
        )

        reality_ids = tuple(r["reality_id"] for r in HISTORICAL_CONSTRAINED_REALITIES_6)
        self.assertEqual(
            reality_ids,
            (
                "R01_google_1999_commodity_cluster_engineer",
                "R02_nasa_apollo_13_1970_survival_engineer",
                "R03_bell_labs_1973_unix_pipe_minimalist",
                "R04_airgapped_zero_network_submarine_harness",
                "R05_high_frequency_microsecond_tick_pipeline",
                "R06_adversarial_byzantine_multi_tenant_marketplace",
            ),
        )

    def test_slot1_triad_lineage_and_12_perspective_envelopes(self) -> None:
        orig = "Every primary write appends a CRC32 frame to local WAL before quorum commit."
        remix = "Speculative quorum WAL pipeline with epoch-fenced follower streaming."
        res = self.rephraser.transform_chunk_across_perspectives(
            chunk_id="chunk_wal_01",
            original_chunk=orig,
            mutated_remix_chunk=remix,
            topic_domain="distributed_consensus",
            request_id="test_slot1_01",
        )
        self.assertTrue(res.accepted)
        self.assertEqual(res.slot_id, SLOT_THINKER_AND_REALITY_REPHRASER)
        self.assertEqual(len(res.layer_verdicts), 7)
        self.assertTrue(all(v == "full" for v in res.layer_verdicts.values()))

        triad = res.output["triad_lineage"]
        self.assertEqual(triad["original_chunk"], orig)
        self.assertEqual(triad["mutated_remix_chunk"], remix)
        self.assertIn("TRIAD_PERSPECTIVE_SYNTHESIS[chunk_wal_01]", triad["perspective_enhanced_chunk"])
        self.assertTrue(triad["triad_complete_and_immutable"])
        self.assertEqual(len(triad["original_chunk_sha256"]), 64)
        self.assertEqual(len(triad["mutated_remix_chunk_sha256"]), 64)
        self.assertEqual(len(triad["perspective_enhanced_chunk_sha256"]), 64)

        self.assertEqual(res.output["personas_evaluated_count"], 6)
        self.assertEqual(res.output["realities_simulated_count"], 6)
        self.assertEqual(res.output["total_perspective_envelopes"], 12)

        marx_entry = [
            p for p in res.output["thinker_persona_rewrites"]
            if p["persona_id"] == "P02_karl_marx_historical_materialist_critique"
        ][0]
        self.assertIn("Karl Marx", marx_entry["rephrased_content"])
        self.assertIn("means of production", marx_entry["rephrased_content"])

        apollo_entry = [
            r for r in res.output["historical_reality_simulations"]
            if r["reality_id"] == "R02_nasa_apollo_13_1970_survival_engineer"
        ][0]
        self.assertEqual(apollo_entry["era_year"], 1970)
        self.assertTrue(apollo_entry["anachronism_free"])

    def test_slot1_fallback_chain_and_idempotency_dedup(self) -> None:
        res_fallback = self.rephraser.transform_chunk_across_perspectives(
            chunk_id="chunk_fb_01",
            original_chunk="Original text",
            mutated_remix_chunk="Remixed text",
            simulate_Compare_failures=REPHRASER_ENGINE_ORDER[:3],
            request_id="test_slot1_fb",
        )
        self.assertTrue(res_fallback.accepted)
        self.assertEqual(res_fallback.selected_engine, ENGINE_DETERMINISTIC_TRIAD_FALLBACK)
        self.assertEqual(len(res_fallback.fallback_chain_tried), 4)

        res_second = self.rephraser.transform_chunk_across_perspectives(
            chunk_id="chunk_fb_01",
            original_chunk="Original text",
            mutated_remix_chunk="Remixed text",
            simulate_Compare_failures=REPHRASER_ENGINE_ORDER[:3],
            request_id="test_slot1_fb",
        )
        self.assertIs(res_fallback, res_second)

    def test_slot2_40_vector_dialectical_challenge_matrix(self) -> None:
        res = self.challenger.challenge_chunk_10x(
            chunk_id="chunk_dial_01",
            original_chunk="Stage-1 MinHash LSH prunes 99.9% of pairs before Gemma 4 verification.",
            mutated_remix_chunk="Cascaded L0 + Jev + Gemma 4 entity blocking pipeline.",
            topic_domain="entity_resolution",
            request_id="test_slot2_01",
        )
        self.assertTrue(res.accepted)
        self.assertEqual(res.slot_id, SLOT_DIALECTICAL_10X_CHALLENGER)
        out = res.output
        self.assertEqual(out["total_dialectical_vectors"], 40)
        self.assertTrue(out["all_scores_calibrated_in_unit_interval"])
        self.assertTrue(out["triad_lineage"]["triad_complete_and_immutable"])

        for quad in DIALECTICAL_QUADRANTS_4:
            items = out[quad]
            self.assertEqual(len(items), 10)
            codes = {item["code"] for item in items}
            self.assertEqual(len(codes), 10)
            for item in items:
                self.assertGreaterEqual(item["confidence_score"], 0.0)
                self.assertLessEqual(item["confidence_score"], 1.0)
                self.assertGreaterEqual(item["severity_score"], 0.0)
                self.assertLessEqual(item["severity_score"], 1.0)

    def test_slot2_fallback_chain_and_thin_component_adapter(self) -> None:
        res_fb = self.challenger.challenge_chunk_10x(
            chunk_id="chunk_dial_fb",
            original_chunk="Original text",
            mutated_remix_chunk="Remixed text",
            simulate_engine_failures=DIALECTICAL_ENGINE_ORDER[:3],
            request_id="test_slot2_fb",
        )
        self.assertTrue(res_fb.accepted)
        self.assertEqual(res_fb.selected_engine, ENGINE_DETERMINISTIC_10X_FALLBACK)

        for slot_obj in (self.rephraser, self.challenger):
            adapter = slot_obj.as_thin_adapter()
            self.assertIsInstance(adapter, ThinComponentAdapter)
            contract = adapter.inspect_contract()
            self.assertEqual(contract["slot_id"], slot_obj.slot_id)
            self.assertLessEqual(contract["adapter_loc"], 30)
            exec_res = adapter.execute(
                {
                    "chunk_id": "thin_01",
                    "original_chunk": "Original via thin adapter",
                    "mutated_remix_chunk": "Remix via thin adapter",
                    "preferred_engine": (
                        ENGINE_HISTORICAL_REALITY_SIMULATOR
                        if slot_obj is self.rephraser
                        else ENGINE_OPERATING_ENVELOPE_STRESS_MATRIX
                    ),
                }
            )
            self.assertTrue(adapter.verify_receipt(exec_res))

    def test_four_known_wrong_refusal_controls(self) -> None:
        kw = run_known_wrong_controls()
        self.assertEqual(kw["total_controls"], 4)
        self.assertEqual(kw["passed_controls"], 4)
        expected_codes = {
            "triad_lineage_corruption_refused",
            "incomplete_or_duplicate_10x_dialectical_matrix_refused",
            "reality_constraint_anachronism_violation_refused",
            "uncalibrated_confidence_score_out_of_bounds_refused",
        }
        actual_codes = {c["actual_refusal_code"] for c in kw["controls"]}
        self.assertEqual(actual_codes, expected_codes)
        for ctrl in kw["controls"]:
            self.assertTrue(ctrl["refused_before_engine"])
            self.assertTrue(ctrl["passed"])

    def test_36_workload_benchmark_vs_baseline(self) -> None:
        workloads = build_36_perspective_challenge_workloads()
        self.assertEqual(len(workloads), 36)

        bench = run_perspective_prism_and_10x_benchmark()
        self.assertEqual(bench["workloads_evaluated"], 36)

        base = bench["single_persona_vanilla_llm_paraphrase_baseline"]
        self.assertEqual(base["engine_id"], BASELINE_SINGLE_PERSONA_PARAPHRASE)
        self.assertEqual(base["viewpoints_per_chunk"], 1)
        self.assertEqual(base["historical_reality_projections"], 0)
        self.assertEqual(base["semantic_self_similarity_mode_collapse_pct"], 82.0)
        self.assertEqual(base["missed_boundary_failure_scenarios_pct"], 78.0)

        suite = bench["baltor_perspective_prism_and_10x_dialectical_challenge_suite"]
        self.assertEqual(suite["engine_id"], BALTOR_PERSPECTIVE_PRISM_AND_10X_SUITE)
        self.assertEqual(suite["combined_perspective_and_reality_envelopes"], "12/12")
        self.assertEqual(suite["dialectical_vectors_per_chunk"], "40/40")
        self.assertEqual(suite["total_personas_applied_across_36_workloads"], 216)
        self.assertEqual(suite["total_realities_simulated_across_36_workloads"], 216)
        self.assertEqual(suite["total_dialectical_vectors_across_36_workloads"], 1440)
        self.assertEqual(suite["triad_lineage_preservation_rate_pct"], 100.0)
        self.assertEqual(suite["calibrated_unit_interval_rate_pct"], 100.0)
        self.assertEqual(suite["corner_case_and_novel_mechanism_lift_pct"], "+340%")


if __name__ == "__main__":
    unittest.main()
