"""Controller-owned workflow definitions."""

from __future__ import annotations

from dataclasses import dataclass

from .domain import Stage, WorkflowDefinitionId


@dataclass(frozen=True, slots=True)
class WorkflowDefinition:
    workflow_definition_id: WorkflowDefinitionId
    stages: tuple[Stage, ...]

    def __post_init__(self) -> None:
        if not self.stages:
            raise ValueError("workflow must contain at least one stage")
        if len(set(self.stages)) != len(self.stages):
            raise ValueError("workflow stages must be unique")

    @property
    def first_stage(self) -> Stage:
        return self.stages[0]

    def next_stage(self, stage: Stage) -> Stage | None:
        try:
            index = self.stages.index(stage)
        except ValueError as exc:
            raise ValueError(f"stage is not part of workflow: {stage}") from exc
        next_index = index + 1
        return self.stages[next_index] if next_index < len(self.stages) else None


PHASE1_WORKFLOW = WorkflowDefinition(
    workflow_definition_id=WorkflowDefinitionId("workflow:project-review-system:phase1:v1"),
    stages=(
        Stage.ADVERSARIAL,
        Stage.INTERDEPENDENCY,
        Stage.NORMALIZATION,
        Stage.STRUCTURAL_OPTIMIZATION,
        Stage.END_TO_END_VALIDATION,
    ),
)
