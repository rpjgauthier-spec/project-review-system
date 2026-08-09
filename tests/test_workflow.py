import unittest

from project_review_system.domain import ProgramState, Stage, WorkflowDefinitionId
from project_review_system.workflow import PHASE1_WORKFLOW, TerminalRules, WorkflowDefinition


class WorkflowTests(unittest.TestCase):
    def test_phase1_stage_order_and_initial_stage_are_exact(self):
        self.assertEqual(PHASE1_WORKFLOW.stages, (
            Stage.ADVERSARIAL, Stage.INTERDEPENDENCY, Stage.NORMALIZATION,
            Stage.STRUCTURAL_OPTIMIZATION, Stage.END_TO_END_VALIDATION,
        ))
        self.assertEqual(PHASE1_WORKFLOW.initial_stage, Stage.ADVERSARIAL)

    def test_terminal_rules_are_explicit(self):
        self.assertEqual(PHASE1_WORKFLOW.terminal_rules.successful_final_state, ProgramState.COMPLETE)
        self.assertEqual(PHASE1_WORKFLOW.terminal_rules.failed_final_state, ProgramState.FAILED)

    def test_next_stage_is_deterministic(self):
        self.assertEqual(PHASE1_WORKFLOW.next_stage(Stage.NORMALIZATION), Stage.STRUCTURAL_OPTIMIZATION)
        self.assertIsNone(PHASE1_WORKFLOW.next_stage(Stage.END_TO_END_VALIDATION))

    def test_workflow_rejects_invalid_definition(self):
        rules = TerminalRules(ProgramState.COMPLETE, ProgramState.FAILED)
        with self.assertRaises(ValueError):
            WorkflowDefinition(WorkflowDefinitionId("workflow:bad"), (Stage.ADVERSARIAL, Stage.ADVERSARIAL), Stage.ADVERSARIAL, rules)
        with self.assertRaises(ValueError):
            WorkflowDefinition(WorkflowDefinitionId("workflow:bad"), (Stage.ADVERSARIAL,), Stage.NORMALIZATION, rules)
        with self.assertRaises(ValueError):
            WorkflowDefinition("workflow:raw", (Stage.ADVERSARIAL,), Stage.ADVERSARIAL, rules)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            PHASE1_WORKFLOW.next_stage("Normalization")  # type: ignore[arg-type]


if __name__ == "__main__": unittest.main()
