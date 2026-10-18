"""Tests for Recursive Leading 5W1H Multi-Persona, Context-Refresh, Confidence/Strength-Scored &
Second-Order Entity Drill-Down (`Elon Musk` Protagonist/Antagonist Dialectics) Information Graph Engine Suite.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

REPOSITORY = Path(__file__).resolve().parents[1]
if str(REPOSITORY / "src") not in sys.path:
    sys.path.insert(0, str(REPOSITORY / "src"))
if str(REPOSITORY / "tools") not in sys.path:
    sys.path.insert(0, str(REPOSITORY / "tools"))

from recursive_5w1h_confidence_graph_and_entity_drilldown_engines import (  # noqa: E402
    ALL_QUESTION_VARIATIONS,
    BALTOR_RECURSIVE_5W1H_GRAPH_SUITE,
    BASELINE_SINGLE_PASS_BASIC_5W1H,
    BENCHMARK_40_TASKS,
    COVERAGE_LAYERS,
    ENGINE_CONTRASTIVE_EPISTEMIC_AGE_PROBE,
    ENGINE_DETERMINISTIC_5W1H_CONFIDENCE_FALLBACK,
    ENGINE_DETERMINISTIC_ENTITY_GRAPH_FALLBACK,
    ENGINE_DIALECTICAL_ENTITY_PRUNER,
    ENGINE_MULTI_ANGLE_5W1H_INTERROGATOR,
    ENGINE_PROTAGONIST_ANTAGONIST_GRAPH,
    ENGINE_SECOND_ORDER_5W1H_EXPANDER,
    ENGINE_STRUCTURED_JSON_YAML_ARRAY,
    EPISTEMIC_AGE_PERSONAS,
    LEADING_5W1H_ENGINE_ORDER,
    RECURSIVE_ENTITY_GRAPH_ENGINE_ORDER,
    SLOT_LEADING_5W1H_INTERROGATOR,
    SLOT_RECURSIVE_ENTITY_GRAPH,
    SUPPORTED_CONTEXT_REFRESH_MODES,
    SUPPORTED_OUTPUT_FORMATS,
    SUPPORTED_POLARITIES,
    WHAT_VARIATIONS,
    WHEN_WHY_HOW_VARIATIONS,
    WHERE_VARIATIONS,
    WHO_VARIATIONS,
    EnvelopeInvocationRequest,
    Leading5W1HPersonaAndConfidenceInterrogatorSlot,
    RecursiveEntityDrilldownProtagonistAntagonistGraphSlot,
    run_known_wrong_controls,
    run_recursive_5w1h_and_entity_graph_benchmark,
)


class Recursive5W1HConfidenceGraphAndEntityDrilldownTest(unittest.TestCase):
    def setUp(self) -> None:
        self.slot1 = Leading5W1HPersonaAndConfidenceInterrogatorSlot()
        self.slot2 = RecursiveEntityDrilldownProtagonistAntagonistGraphSlot(self.slot1)

    def test_slot1_all_5w1h_variations_personas_and_parseable_formats(self) -> None:
        res = self.slot1.interrogate_chunk(
            "chunk_telemetry_01",
            "Hardware-in-the-loop rocket stage telemetry and SQLite WAL durability under 10ms deadlines.",
            output_format="JSON",
            request_id="test_slot1_full",
        )
        self.assertTrue(res.accepted)
        self.assertEqual(res.slot_id, SLOT_LEADING_5W1H_INTERROGATOR)
        self.assertEqual(res.selected_engine, ENGINE_MULTI_ANGLE_5W1H_INTERROGATOR)
        self.assertTrue(self.slot1.adapter.verify_receipt(res))

        for layer in COVERAGE_LAYERS:
            self.assertEqual(res.layer_verdicts[layer], "full")

        out = res.output
        self.assertEqual(tuple(out["variations_covered"]), ALL_QUESTION_VARIATIONS)
        self.assertEqual(out["who_variations_count"], len(WHO_VARIATIONS))
        self.assertEqual(out["what_variations_count"], len(WHAT_VARIATIONS))
        self.assertEqual(out["where_variations_count"], len(WHERE_VARIATIONS))
        self.assertEqual(out["when_why_how_variations_count"], len(WHEN_WHY_HOW_VARIATIONS))
        self.assertEqual(tuple(out["epistemic_age_personas_covered"]), EPISTEMIC_AGE_PERSONAS)
        self.assertEqual(tuple(out["context_refresh_modes_covered"]), SUPPORTED_CONTEXT_REFRESH_MODES)
        self.assertEqual(tuple(out["polarities_covered"]), SUPPORTED_POLARITIES)

        var_outputs = out["variation_outputs"]
        self.assertEqual(len(var_outputs["who_top_10_ranked"]), 10)
        self.assertEqual(len(var_outputs["what_of_top_10_ranked"]), 10)

        # Verify contrastive NOT polarity
        for item in var_outputs["who_does_not_relate_contrastive"]:
            self.assertEqual(item["polarity"], "does_not_relate_to")
            self.assertGreaterEqual(item["confidence"], 0.0)
            self.assertLessEqual(item["confidence"], 1.0)
            self.assertGreaterEqual(item["strength"], 0.0)
            self.assertLessEqual(item["strength"], 1.0)

        # Verify epistemic-age personas (kindergartener, high-schooler, domain-expert)
        age_lenses = [x["persona_lens"] for x in var_outputs["who_by_epistemic_age_persona"]]
        self.assertEqual(tuple(age_lenses), EPISTEMIC_AGE_PERSONAS)

        # Verify JSON, YAML, and TypedFunctionCallList formats are populated and parseable
        serialized = out["serialized_formats"]
        for fmt in SUPPORTED_OUTPUT_FORMATS:
            self.assertIn(fmt, serialized)
        parsed_json = json.loads(serialized["JSON"])
        self.assertEqual(len(parsed_json), out["total_scored_candidates"])
        self.assertTrue(serialized["YAML"].startswith("candidates:\n  - candidate_id:"))
        self.assertEqual(len(serialized["TypedFunctionCallList"]), out["total_scored_candidates"])

    def test_slot2_recursive_entity_drilldown_elon_musk_and_antagonist_pruning(self) -> None:
        res = self.slot2.build_recursive_entity_graph(
            "chunk_starbase_wal_02",
            "Iterative telemetry loop with strict amp-hour and SQLite WAL durability guarantees.",
            requested_recursion_depth=2,
            request_id="test_slot2_graph",
        )
        self.assertTrue(res.accepted)
        self.assertEqual(res.slot_id, SLOT_RECURSIVE_ENTITY_GRAPH)
        self.assertEqual(res.selected_engine, ENGINE_PROTAGONIST_ANTAGONIST_GRAPH)
        self.assertTrue(self.slot2.adapter.verify_receipt(res))

        out = res.output
        self.assertTrue(out["elon_musk_subtree_verified"])
        self.assertGreaterEqual(out["spurious_edges_pruned"], 1)
        self.assertLess(out["per_node_latency_ms"], 12.0)

        subtrees = {st["entity_name"]: st for st in out["dialectical_entity_subtrees"]}
        self.assertIn("Elon Musk", subtrees)
        self.assertIn("NASA Apollo 13 Mission Control", subtrees)
        self.assertIn("SQLite WAL Coordinator", subtrees)
        self.assertIn("Overseas Migrant Worker", subtrees)
        self.assertIn("Spurious Celebrity Meme Coin", subtrees)

        elon = subtrees["Elon Musk"]
        expected_net = round(
            elon["protagonist_defense_probe"]["protagonist_strength"]
            * elon["protagonist_defense_probe"]["confidence"]
            - 0.5 * elon["antagonist_rebuttal_probe"]["antagonist_rebuttal_strength"],
            4,
        )
        self.assertEqual(elon["net_strength"], expected_net)
        self.assertTrue(elon["promoted_to_core_graph"])

        spurious = subtrees["Spurious Celebrity Meme Coin"]
        self.assertFalse(spurious["promoted_to_core_graph"])
        self.assertTrue(spurious["antagonist_rebuttal_probe"]["falsified"])

        graph = out["information_graph"]
        self.assertEqual(len(graph["edges"]), 4)
        self.assertEqual(len(graph["recurring_scenarios_ranked"]), 4)
        # Highest net_strength should be ranked first
        strengths = [s["net_strength"] for s in graph["recurring_scenarios_ranked"]]
        self.assertEqual(strengths, sorted(strengths, reverse=True))

    def test_engine_fallback_chains_and_idempotency(self) -> None:
        # Slot 1 fallback to terminal engine
        res1 = self.slot1.interrogate_chunk(
            "chunk_fb_1",
            "Fallback check chunk.",
            simulate_Compare_failures=(
                ENGINE_MULTI_ANGLE_5W1H_INTERROGATOR,
                ENGINE_CONTRASTIVE_EPISTEMIC_AGE_PROBE,
                ENGINE_STRUCTURED_JSON_YAML_ARRAY,
            ),
            request_id="req_fb_slot1",
        )
        self.assertTrue(res1.accepted)
        self.assertEqual(res1.selected_engine, ENGINE_DETERMINISTIC_5W1H_CONFIDENCE_FALLBACK)
        self.assertEqual(res1.fallback_chain_tried, LEADING_5W1H_ENGINE_ORDER)

        # Slot 2 fallback to terminal engine
        res2 = self.slot2.build_recursive_entity_graph(
            "chunk_fb_2",
            "Fallback check graph.",
            simulate_engine_failures=(
                ENGINE_PROTAGONIST_ANTAGONIST_GRAPH,
                ENGINE_DIALECTICAL_ENTITY_PRUNER,
                ENGINE_SECOND_ORDER_5W1H_EXPANDER,
            ),
            request_id="req_fb_slot2",
        )
        self.assertTrue(res2.accepted)
        self.assertEqual(res2.selected_engine, ENGINE_DETERMINISTIC_ENTITY_GRAPH_FALLBACK)
        self.assertEqual(res2.fallback_chain_tried, RECURSIVE_ENTITY_GRAPH_ENGINE_ORDER)

        # SHA-256 idempotency deduplication check
        res2_dup = self.slot2.build_recursive_entity_graph(
            "chunk_fb_2",
            "Fallback check graph.",
            simulate_engine_failures=(
                ENGINE_PROTAGONIST_ANTAGONIST_GRAPH,
                ENGINE_DIALECTICAL_ENTITY_PRUNER,
                ENGINE_SECOND_ORDER_5W1H_EXPANDER,
            ),
            request_id="req_fb_slot2",
        )
        self.assertIs(res2, res2_dup)

    def test_carrier_and_handshake_refusals(self) -> None:
        bad_carrier = self.slot1.adapter.execute(
            EnvelopeInvocationRequest(
                slot_id=SLOT_LEADING_5W1H_INTERROGATOR,
                request_id="   ",
                payload={"chunk_id": "c", "chunk_text": "t"},
                preferred_engine=ENGINE_MULTI_ANGLE_5W1H_INTERROGATOR,
            )
        )
        self.assertFalse(bad_carrier.accepted)
        self.assertIsNotNone(bad_carrier.refusal)
        self.assertEqual(bad_carrier.refusal.code, "carrier_request_id_missing")

        bad_handshake = self.slot1.adapter.execute(
            EnvelopeInvocationRequest(
                slot_id=SLOT_LEADING_5W1H_INTERROGATOR,
                request_id="req_hs_bad",
                payload={"chunk_id": "c", "chunk_text": "t"},
                preferred_engine=ENGINE_MULTI_ANGLE_5W1H_INTERROGATOR,
                protocol_version="99.9",
            )
        )
        self.assertFalse(bad_handshake.accepted)
        self.assertIsNotNone(bad_handshake.refusal)
        self.assertEqual(bad_handshake.refusal.code, "protocol_version_incompatible")

    def test_four_known_wrong_refusal_controls(self) -> None:
        kw = run_known_wrong_controls()
        self.assertEqual(kw["total_controls"], 4)
        self.assertEqual(kw["passed_controls"], 4)
        expected_codes = {
            "missing_confidence_or_strength_scores_refused",
            "unbounded_entity_recursion_depth_refused",
            "antagonist_falsified_spurious_connection_refused",
            "unparseable_interrogation_output_format_refused",
        }
        actual_codes = {c["actual_refusal_code"] for c in kw["controls"]}
        self.assertEqual(actual_codes, expected_codes)
        for ctrl in kw["controls"]:
            self.assertTrue(ctrl["refused_before_engine"])
            self.assertTrue(ctrl["passed"])

    def test_40_task_benchmark_metrics(self) -> None:
        self.assertEqual(len(BENCHMARK_40_TASKS), 40)
        bench = run_recursive_5w1h_and_entity_graph_benchmark()
        self.assertEqual(bench["tasks_evaluated"], 40)
        self.assertEqual(bench["without_baltor_baseline"]["engine_id"], BASELINE_SINGLE_PASS_BASIC_5W1H)

        with_baltor = bench["with_baltor_recursive_5w1h_graph_suite"]
        self.assertEqual(with_baltor["engine_id"], BALTOR_RECURSIVE_5W1H_GRAPH_SUITE)
        self.assertEqual(with_baltor["parseable_output_compliance_pct"], "100.0%")
        self.assertEqual(with_baltor["multi_hop_entity_discovery_multiplier"], "6.8x")
        self.assertEqual(with_baltor["dialectically_promoted_second_order_edges"], 160)
        self.assertEqual(with_baltor["spurious_edges_filtered_by_antagonist"], 40)
        self.assertTrue(with_baltor["sub_12ms_per_node_achieved"])


if __name__ == "__main__":
    unittest.main()
