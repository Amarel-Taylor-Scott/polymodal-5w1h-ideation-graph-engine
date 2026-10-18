"""Tests and known-wrong controls for the Universal Poly-Modal & Scale-Invariant
Hierarchical Ingestor, Infinite Sub-Partitioner, Clutter-Cutter & Cross-Modal
(`Chunk <-> Image` + Multilingual + RAG/Embedding) Mutation Engine Suite.
"""
from __future__ import annotations

from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
if str(HERE.parent / "src") not in sys.path:
    sys.path.insert(0, str(HERE.parent / "src"))

import universal_polymodal_hierarchical_chunk_mutator_engines as pm  # noqa: E402
from loop_engine.core.engines.envelope import COVERAGE_LAYERS, LAYER_REFUSED  # noqa: E402


class UniversalPolymodalHierarchicalChunkMutatorTests(unittest.TestCase):
    """Verify Slot Family 1, Slot Family 2, 36-workload benchmark, and 4 known-wrong controls."""

    def test_slot1_polymodal_chunking_engines_strategies_and_immutable_root(self) -> None:
        contract = pm.UNIVERSAL_POLYMODAL_CHUNKING_ADAPTER.inspect_contract()
        self.assertEqual(contract["slot_id"], pm.SLOT_UNIVERSAL_POLYMODAL_CHUNKING)
        self.assertLess(int(contract["loc"]), 30)

        sample = pm.ALL_36_POLYMODAL_CHUNK_MUTATION_WORKLOADS[0]
        for idx, eng in enumerate(pm.POLYMODAL_CHUNKING_ENGINE_ORDER):
            res = pm.invoke_universal_polymodal_chunking_slot(
                sample,
                request_id=f"test_slot1_eng_{idx}",
                preferred_engine=eng,
            )
            self.assertTrue(res.accepted)
            self.assertEqual(res.selected_engine, eng)
            self.assertTrue(pm.UNIVERSAL_POLYMODAL_CHUNKING_ADAPTER.verify_receipt(res))
            out = res.output
            self.assertEqual(tuple(out["strategies_executed"]), pm.PARTITIONING_7_STRATEGIES)
            self.assertTrue(out["all_nodes_preserve_root_hash"])
            self.assertGreaterEqual(int(out["max_hierarchy_depth"]), 5)
            self.assertLess(float(out["mean_window_latency_ms"]), 18.0)
            self.assertLess(float(out["peak_window_memory_mb"]), 50.0)
            for layer in COVERAGE_LAYERS:
                self.assertEqual(res.layer_verdicts[layer], "full")

            # Verify P3 photo-in-page and photo-in-paragraph spatial coordinates and caption binding
            p3_nodes = out["nodes_by_strategy"]["P3_photos_within_pages_and_paragraphs"]
            self.assertEqual(len(p3_nodes), 2)
            self.assertIsNotNone(p3_nodes[0]["spatial_bbox"])
            self.assertTrue(p3_nodes[1]["caption_binding"].startswith("Inline Sub-Figure"))

            # Verify P6 clutter cutter strips filler words while preserving NEVER and numeric bounds
            p6_report = out["clutter_cutter_report"]
            self.assertGreaterEqual(int(p6_report["fluff_phrases_removed"]), 1)
            self.assertIn("NEVER", p6_report["preserved_negations"])
            self.assertTrue(any("12ms" in b for b in p6_report["preserved_numeric_bounds"]))

    def test_slot2_cross_modal_multilingual_and_rag_mutation_engines(self) -> None:
        contract = pm.CHUNK_MUTATION_TRANSCODER_ADAPTER.inspect_contract()
        self.assertEqual(contract["slot_id"], pm.SLOT_CHUNK_MUTATION_TRANSCODER)
        self.assertLess(int(contract["loc"]), 30)

        sample = pm.ALL_36_POLYMODAL_CHUNK_MUTATION_WORKLOADS[5]
        for idx, eng in enumerate(pm.CHUNK_MUTATION_ENGINE_ORDER):
            res = pm.invoke_chunk_mutation_transcoder_slot(
                sample,
                request_id=f"test_slot2_eng_{idx}",
                preferred_engine=eng,
            )
            self.assertTrue(res.accepted)
            self.assertEqual(res.selected_engine, eng)
            self.assertTrue(pm.CHUNK_MUTATION_TRANSCODER_ADAPTER.verify_receipt(res))
            out = res.output
            self.assertTrue(out["original_provenance_100pct_intact"])
            self.assertTrue(out["bidirectional_transcoding_verified"])
            self.assertEqual(tuple(out["languages_covered"]), pm.TARGET_MUTATION_LANGUAGES)
            self.assertEqual(tuple(out["supported_2026_models"]), pm.SUPPORTED_2026_MODELS)
            self.assertGreaterEqual(int(out["total_mutated_siblings"]), 12)

            siblings = out["mutated_sibling_chunks"]
            cross_modal = [s for s in siblings if s["mutation_kind"] == "bidirectional_chunk_to_image_and_image_to_text"]
            self.assertTrue(len(cross_modal) >= 1)
            self.assertIn("<svg", cross_modal[0]["chunk_to_image_svg_spec"])
            self.assertEqual(
                cross_modal[0]["image_to_text_dense_ocr_graph"]["vision_model_family"],
                "Qwen3.5-VL",
            )

    def test_36_workload_benchmark_and_8000_page_streaming_bounds(self) -> None:
        bench = pm.run_universal_polymodal_chunk_mutator_benchmark()
        self.assertEqual(bench["workloads_evaluated"], 36)
        self.assertEqual(bench["modalities_count"], 6)
        self.assertEqual(bench["strategies_count"], 7)

        base = bench["without_baltor_baseline"]
        self.assertEqual(base["engine_id"], pm.BASELINE_FIXED_512_NAIVE_SPLITTER)
        self.assertEqual(base["modalities_supported"], "1/6")
        self.assertEqual(base["massive_8000_page_status"], "oom_or_timeout")

        suite = bench["with_baltor_polymodal_suite"]
        self.assertEqual(suite["engine_id"], pm.BALTOR_UNIVERSAL_POLYMODAL_CHUNK_MUTATION_SUITE)
        self.assertEqual(suite["modalities_supported"], "6/6")
        self.assertEqual(suite["strategies_supported"], "7/7")
        self.assertEqual(suite["immutable_original_provenance_preservation_pct"], "100.0%")
        self.assertTrue(suite["massive_8000_page_window_latency_within_18ms"])
        self.assertTrue(suite["peak_window_memory_within_50mb"])
        self.assertEqual(suite["downstream_ideation_feature_diversity_multiplier"], "4.4x")

    def test_four_known_wrong_controls_refuse_at_preflight_layer(self) -> None:
        kw = pm.run_known_wrong_controls()
        self.assertEqual(kw["total_controls"], 4)
        self.assertEqual(kw["passed_controls"], 4)
        for ctrl in kw["controls"]:
            self.assertTrue(ctrl["passed"], msg=f"Control failed: {ctrl}")
            self.assertTrue(ctrl["refused_before_engine"])

        # Direct check on cyclic DAG edge detection
        cyclic_res = pm.invoke_universal_polymodal_chunking_slot(
            {
                "doc_id": "direct_cycle_doc",
                "dag_edges": (("n0", "n1"), ("n1", "n2"), ("n2", "n0")),
            },
            request_id="direct_cycle_probe",
        )
        self.assertFalse(cyclic_res.accepted)
        self.assertIsNotNone(cyclic_res.refusal)
        self.assertEqual(cyclic_res.refusal.code, "cyclic_hierarchical_chunk_dag_refused")
        self.assertEqual(cyclic_res.layer_verdicts["preflight"], LAYER_REFUSED)


if __name__ == "__main__":
    unittest.main()
