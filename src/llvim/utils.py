import logging
import time
from enum import Enum
from typing import Generic, TypeVar

EnumT = TypeVar("EnumT", bound=Enum)


class PipelineManager(Generic[EnumT]):
    def __init__(self, process_until: EnumT | None = None):
        self.stage_to_elapsed_time: dict[EnumT, float] = {}
        self.process_until = process_until
        self.last_time = None
        self.current_stage = None

    def start_stage(self, stage: EnumT) -> bool:
        """Start a new stage, previous stage must be complete."""
        assert self.current_stage is None
        now = time.time()
        self.last_time = now
        self.current_stage = stage
        if self.process_until and stage == self.process_until:
            logging.info(
                f"Halting pipeline at stage: {self.process_until.name} per `process_until` config."
            )
            return False  # halt
        return True  # continue

    def end_stage(self):
        """End the current stage using the provided end time."""
        assert self.current_stage
        assert self.last_time is not None
        self.stage_to_elapsed_time[self.current_stage] = time.time() - self.last_time
        logging.info(
            f"Finished stage: {self.current_stage.name} in {self.stage_to_elapsed_time[self.current_stage]:.2f} seconds."
        )
        self.current_stage = None

    def get_elapsed_time_for_stage(self, stage: EnumT) -> float | None:
        return self.stage_to_elapsed_time.get(stage, None)

    def get_time_up_to_stage(self, stage: EnumT) -> float:
        prev_stages = [
            prev_stage for prev_stage in type(stage) if prev_stage.value < stage.value
        ]
        assert all(
            self.get_elapsed_time_for_stage(prev_stage) is not None
            for prev_stage in prev_stages
        )
        return sum(self.stage_to_elapsed_time[prev_stage] for prev_stage in prev_stages)
