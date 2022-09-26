from typing import List

SMALL_MISTAKE_THRESHOLD = 1 / 50
BIG_MISTAKE_THRESHOLD = 1 / 20


class Competitor:
    def __init__(self, splits: List[int], name: str) -> None:
        self.splits = splits
        self.name = name
        self.total_time = sum(splits)
        self.adjustment_factor = 1.0
        self.losses: List[float] = []


class Course:
    def __init__(self, competitors: List[Competitor]) -> None:
        self.competitors = competitors
        self.num_controls = len(competitors[0].splits)

    def set_adjustments(self) -> None:
        """Calculate time adjustment factors.

        This adjustment normalizes each competitor's splits
        based on their overall speed.

        If this method is not called, times will not be adjusted.
        """

        best_time = min(c.total_time for c in self.competitors)
        for c in self.competitors:
            c.adjustment_factor = best_time / c.total_time

    def calculate_losses(self) -> None:
        for i in range(self.num_controls):
            best_split = min(c.splits[i] for c in self.competitors)  # not adjusted
            adjusted_splits = [c.splits[i] * c.adjustment_factor for c in self.competitors]
            for c, adjusted_split in zip(self.competitors, adjusted_splits):
                # because of adjustments, the loss may be negative
                # this does not matter
                c.losses.append(adjusted_split - best_split)
