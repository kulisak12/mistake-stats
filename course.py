from typing import List

SMALL_MISTAKE_THRESHOLD = 1.0
BIG_MISTAKE_THRESHOLD = 3.0


class Competitor:
    def __init__(self, splits: List[int], name: str) -> None:
        self.splits = splits
        self.name = name
        self.total_time = sum(splits)
        self.losses: List[int] = []

    def made_mistake(self, control: int, threshold: float) -> bool:
        relative_loss = self.losses[control] / self.total_time
        return relative_loss > threshold


class Course:
    def __init__(self, competitors: List[Competitor]) -> None:
        self.competitors = competitors
        self.num_controls = len(competitors[0].splits)

    def calculate_losses(self) -> None:
        for i in range(self.num_controls):
            control_splits = [c.splits[i] for c in self.competitors]
            best_split = min(control_splits)
            for c, split in zip(self.competitors, control_splits):
                c.losses.append(split - best_split)
