"""Controller-owned workflow definitions."""

from __future__ import annotations

from dataclasses import dataclass

from .domain import ProgramState, Stage, WorkflowDefinitionId


@dataclass(frozen=True, slots=True)
class TerminalRules:
    successful_final_state: ProgramState
    failed_final_state: ProgramState

    def __post_init__(self) -> None:
        if self.successful_final_state is not ProgramState.COMPLETE:
            raise ValueError("successful_final_state must be ProgramState.COMPLETE")
        if self.failed_final_state is not ProgramState.FAILED:
            raise ValueError("failed_final_state must be ProgramState.FAILED")


@dataclass(frozen=True, slots=True)
class WorkflowDefinition:
    workflow_definition_id: WorkflowDefinitionId
    stages: tuple[Stage, ...]
    initial_stage: Stage
    terminal_rules: TerminalRules

    def __post_init__(self) -> None:
        if not isinstance(self.workflow_definition_id, WorkflowDefinitionId):
            raise ValueError("workflow_definition_id must be a WorkflowDefinitionId")
        if not isinstance(self.stages, tuple):
            raise ValueError("workflow stages must be an immutable tuple")
        if not self.stages:
            raise ValueError("workflow must contain at least one stage")
        if not all(isinstance(stage, Stage) for stage in self.stages):
            raise ValueError("workflow stages must contain only Stage members")
        if len(set(self.stages)) != len(self.stages):
            raise ValueError("workflow stages must be unique")
        if not isinstance(self.initial_stage, Stage) or self.initial_stage != self.stages[0]:
            raise ValueError("initial_stage must equal the first workflow stage")
        if not isinstance(self.terminal_rules, TerminalRules):
            raise ValueError("terminal_rules must be TerminalRules")

    @property
    def first_stage(self) -> Stage:
        return self.initial_stage

    def next_stage(self, stage: Stage) -> Stage | None:
        if not isinstance(stage, Stage):
            raise ValueError("stage must be a Stage")
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
    initial_stage=Stage.ADVERSARIAL,
    terminal_rules=TerminalRules(
        successful_final_state=ProgramState.COMPLETE,
        failed_final_state=ProgramState.FAILED,
    ),
)
