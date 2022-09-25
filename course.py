import statistics
from typing import List

SMALL_MISTAKE_THRESHOLD = 1.0
BIG_MISTAKE_THRESHOLD = 3.0


class Competitor:

    def __init__(self, splits: List[int]) -> None:
        self.splits = splits
        self.total_time = sum(splits)
        self.adjustment_factor = 1.0
        self.relative_splits: List[float] = []
        self.z_scores: List[float] = []


class Course:
    def __init__(self, competitors: List[Competitor]) -> None:
        self.competitors = competitors
        self.num_controls = len(competitors[0].splits)

    def set_adjustments(self) -> None:
        """Calculate time adjustment factors.

        This adjustment normalizes each competitor's splits
        based on their overall speed.
        """

        best_time = min(c.total_time for c in self.competitors)
        for c in self.competitors:
            c.adjustment_factor = best_time / c.total_time

    def set_relative_splits(self) -> None:
        for i in range(self.num_controls):
            adjusted_splits = [c.splits[i] * c.adjustment_factor for c in self.competitors]
            best_split = min(adjusted_splits)
            for c, split in zip(self.competitors, adjusted_splits):
                c.relative_splits.append(split / best_split)

    def calculate_z_scores(self) -> None:
        for i in range(self.num_controls):
            relative_splits = [c.relative_splits[i] for c in self.competitors]
            z_scores = z_score(relative_splits)
            for c, z in zip(self.competitors, z_scores):
                c.z_scores.append(z)


def z_score(data: List[float]) -> List[float]:
    mean = statistics.mean(data)
    sd = statistics.stdev(data)
    return [(x - mean) / sd for x in data]


def remove_outliers(
    data: List[float],
    threshold_low=-float('inf'),
    threshold_high=float('inf')
) -> List[float]:
    return [
        x for x, z in zip(data, z_score(data))
        if threshold_low <= z <= threshold_high
    ]
