import unittest

from project_review_system.domain import Stage, WorkflowDefinitionId
from project_review_system.workflow import PHASE1_WORKFLOW, WorkflowDefinition


class WorkflowTests(unittest.TestCase):
    def test_phase1_stage_order_is_exact(self) -> None:
        self.assertEqual(
            PHASE1_WORKFLOW.stages,
            (
                Stage.ADVERSARIAL,
                Stage.INTERDEPENDENCY,
                Stage.NORMALIZATION,
                Stage.STRUCTURAL_OPTIMIZATION,
                Stage.END_TO_END_VALIDATION,
            ),
        )

    def test_next_stage_is_deterministic(self) -> None:
        self.assertEqual(
            PHASE1_WORKFLOW.next_stage(Stage.NORMALIZATION),
            Stage.STRUCTURAL_OPTIMIZATION,
        )
        self.assertIsNone(PHASE1_WORKFLOW.next_stage(Stage.END_TO_END_VALIDATION))

    def test_workflow_rejects_duplicate_stages(self) -> None:
        with self.assertRaises(ValueError):
            WorkflowDefinition(
                workflow_definition_id=WorkflowDefinitionId("workflow:bad"),
                stages=(Stage.ADVERSARIAL, Stage.ADVERSARIAL),
            )


if __name__ == "__main__":
    unittest.main()
