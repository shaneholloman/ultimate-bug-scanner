#!/usr/bin/env python3
"""Unit checks for the rule-quality harness invariants."""

import unittest

import rule_quality_harness


class RuleInventoryCoverageInvariantTest(unittest.TestCase):
    def test_accepts_fully_covered_rule_inventory(self) -> None:
        rule_quality_harness.assert_rule_inventory_fully_covered(
            [
                {
                    "label": "rust-rule-pack",
                    "corpus_result_rule_ids_without_generated_rule": [],
                    "uncovered_generated_rule_ids": [],
                }
            ]
        )

    def test_rejects_generated_rule_without_corpus_hit(self) -> None:
        with self.assertRaisesRegex(AssertionError, "rust.new-rule"):
            rule_quality_harness.assert_rule_inventory_fully_covered(
                [
                    {
                        "label": "rust-rule-pack",
                        "corpus_result_rule_ids_without_generated_rule": [],
                        "uncovered_generated_rule_ids": ["rust.new-rule"],
                    }
                ]
            )

    def test_rejects_corpus_rule_without_dumped_rule(self) -> None:
        with self.assertRaisesRegex(AssertionError, "js.ghost-rule"):
            rule_quality_harness.assert_rule_inventory_fully_covered(
                [
                    {
                        "label": "js-rule-pack",
                        "corpus_result_rule_ids_without_generated_rule": ["js.ghost-rule"],
                        "uncovered_generated_rule_ids": [],
                    }
                ]
            )


class RunManifestExpectationTest(unittest.TestCase):
    def test_extract_json_summary_skips_jsonl_findings(self) -> None:
        stdout = "\n".join(
            [
                '{"ruleId":"js.eval-call","severity":"critical","message":"eval"}',
                '{"project":"fixture","totals":{"files":1,"critical":2,"warning":3,"info":4}}',
                "trailing text",
            ]
        )

        summary = rule_quality_harness.extract_json_from_stdout(stdout)

        self.assertIsNotNone(summary)
        self.assertEqual(summary["totals"]["critical"], 2)
        self.assertEqual(summary["totals"]["warning"], 3)

    def test_parse_toon_summary_sums_scanner_totals(self) -> None:
        stdout = "\n".join(
            [
                "scanners[",
                "  scanner: js",
                "  critical: 1",
                "  warning: 2",
                "  info: 3",
                "  files: 4",
                "  scanner: rust",
                "  critical: 5",
                "  warning: 6",
                "  info: 7",
                "  files: 8",
                "]",
                "findings[",
                "]",
            ]
        )

        summary = rule_quality_harness.parse_toon_summary(stdout, "fixture")

        self.assertIsNotNone(summary)
        self.assertEqual(
            summary["totals"],
            {"critical": 6, "warning": 8, "info": 10, "files": 12},
        )

    def test_check_expectations_derives_fail_on_warning_exit(self) -> None:
        errors = rule_quality_harness.check_expectations(
            {"exit_code": "zero"},
            exit_code=0,
            summary={"totals": {"critical": 0, "warning": 1, "info": 0, "files": 1}},
            stdout="",
            stderr="",
            fail_on_warning=True,
        )

        self.assertIn("expected exit 0 but derived 1", errors)

    def test_check_expectations_enforces_substrings_and_totals(self) -> None:
        errors = rule_quality_harness.check_expectations(
            {
                "totals": {
                    "critical": {"min": 1},
                    "warning": {"max": 0},
                },
                "require_substrings": ["must appear"],
                "forbid_substrings": ["must not appear"],
            },
            exit_code=0,
            summary={"totals": {"critical": 0, "warning": 2, "info": 0, "files": 1}},
            stdout="must not appear",
            stderr="",
            fail_on_warning=False,
        )

        self.assertIn("critical count 0 < min 1", errors)
        self.assertIn("warning count 2 > max 0", errors)
        self.assertIn("missing substring 'must appear' in stdout", errors)
        self.assertIn("forbidden substring 'must not appear' present in stdout", errors)


class ScopeConstructionTest(unittest.TestCase):
    @staticmethod
    def case(case_id: str, language: str, tags: list[str]) -> dict[str, object]:
        return {
            "expect": {},
            "id": case_id,
            "language": language,
            "path": f"test-suite/{language}/{case_id}",
            "tags": tags,
        }

    def test_runtime_campaign_scope_uses_target_pairs_and_behavior_cases(self) -> None:
        pairs = [
            {"buggy_case": "js-buggy", "clean_case": "js-clean", "language": "js"},
            {
                "buggy_case": "python-buggy",
                "clean_case": "python-clean",
                "language": "python",
            },
        ]
        cases = [
            self.case("js-behavior-buggy", "js", ["async", "buggy"]),
            self.case("golang-behavior-clean", "golang", ["resource", "clean"]),
            self.case("rust-security-excluded", "rust", ["async", "security", "buggy"]),
            self.case("python-behavior-buggy", "python", ["async", "buggy"]),
        ]

        scopes = rule_quality_harness.runtime_scopes_from_pairs(pairs, cases)

        self.assertEqual(
            scopes["campaign"],
            [
                "js-buggy",
                "js-clean",
                "js-behavior-buggy",
                "golang-behavior-clean",
            ],
        )
        self.assertEqual(
            scopes["all"],
            ["js-buggy", "js-clean", "python-buggy", "python-clean"],
        )

    def test_robustness_campaign_clean_fuzz_scope_uses_clean_target_cases(self) -> None:
        pairs = [
            {"buggy_case": "rust-buggy", "clean_case": "rust-clean", "language": "rust"},
            {
                "buggy_case": "python-buggy",
                "clean_case": "python-clean",
                "language": "python",
            },
        ]
        cases = [
            self.case("js-behavior-buggy", "js", ["type-narrowing", "buggy"]),
            self.case("js-behavior-clean", "js", ["type-narrowing", "clean"]),
            self.case("python-behavior-clean", "python", ["type-narrowing", "clean"]),
        ]

        scopes = rule_quality_harness.robustness_scopes_from_pairs(pairs, cases)

        self.assertEqual(
            scopes["campaign"]["metamorphic"],
            ["rust-buggy", "rust-clean", "js-behavior-buggy", "js-behavior-clean"],
        )
        self.assertEqual(
            scopes["campaign"]["clean_fuzz"],
            ["rust-clean", "js-behavior-clean"],
        )


class TargetCleanBaselineBudgetTest(unittest.TestCase):
    @staticmethod
    def baseline_case(
        case_id: str,
        warning_max: int = 0,
        forbid_substrings: list[str] | None = None,
    ) -> dict[str, object]:
        expect: dict[str, object] = {
            "exit_code": "zero",
            "totals": {
                "critical": {"max": 0},
                "warning": {"max": warning_max},
            },
        }
        if forbid_substrings is not None:
            expect["forbid_substrings"] = forbid_substrings
        return {
            "expect": expect,
            "id": case_id,
            "language": case_id.split("-", 1)[0],
            "path": f"test-suite/{case_id}",
            "tags": ["clean"],
        }

    def test_rejects_missing_target_clean_baseline_case(self) -> None:
        cases = [
            self.baseline_case(case_id)
            for case_id in rule_quality_harness.TARGET_CLEAN_BASELINE_CASE_IDS[:-1]
        ]

        with self.assertRaisesRegex(AssertionError, "rust-clean"):
            rule_quality_harness.target_clean_baseline_budgets(cases)

    def test_records_target_clean_warning_budget_and_forbid_counts(self) -> None:
        cases = [
            self.baseline_case(
                case_id,
                warning_max=2 if case_id == "js-module-clean" else 0,
                forbid_substrings=["danger", "panic"] if case_id == "rust-clean" else [],
            )
            for case_id in rule_quality_harness.TARGET_CLEAN_BASELINE_CASE_IDS
        ]

        budget = rule_quality_harness.target_clean_baseline_budgets(cases)

        self.assertEqual(
            budget["case_count"],
            len(rule_quality_harness.TARGET_CLEAN_BASELINE_CASE_IDS),
        )
        self.assertEqual(
            budget["strict_zero_case_count"],
            len(rule_quality_harness.TARGET_CLEAN_BASELINE_CASE_IDS) - 1,
        )
        self.assertEqual(budget["warning_budget_total"], 2)
        rust_case = next(case for case in budget["cases"] if case["id"] == "rust-clean")
        self.assertEqual(rust_case["forbid_substring_count"], 2)


class ExpectationStrengthScopeTest(unittest.TestCase):
    def test_language_filter_separates_target_and_all_supported_debt(self) -> None:
        runtime_scopes = {"all": ["js-clean", "python-clean"]}
        cases = [
            {
                "expect": {
                    "exit_code": "zero",
                    "forbid_substrings": ["JS warning text"],
                    "totals": {"critical": {"max": 0}, "warning": {"max": 0}},
                },
                "id": "js-clean",
                "language": "js",
                "path": "test-suite/js/clean/example.js",
                "tags": ["js", "clean"],
            },
            {
                "expect": {
                    "exit_code": "zero",
                    "totals": {"critical": {"max": 0}, "warning": {"max": 2}},
                },
                "id": "python-clean",
                "language": "python",
                "path": "test-suite/python/clean/example.py",
                "tags": ["python", "clean"],
            },
        ]

        target = rule_quality_harness.expectation_strength_scopes_from_runtime(
            runtime_scopes,
            cases,
            {"js"},
        )
        all_supported = rule_quality_harness.expectation_strength_scopes_from_runtime(
            runtime_scopes,
            cases,
            {"js", "python"},
        )

        self.assertEqual(target["all"]["weak_case_count"], 0)
        self.assertEqual(all_supported["all"]["weak_case_count"], 1)
        self.assertEqual(
            all_supported["all"]["weak_cases"][0]["reasons"],
            [
                "clean_missing_forbid_substrings",
                "clean_not_strict_zero_critical_warning",
            ],
        )


if __name__ == "__main__":
    unittest.main()
