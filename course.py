import statistics
from typing import List

TOO_FAST_THRESHOLD = -3.0
SMALL_MISTAKE_THRESHOLD = 1.0
BIG_MISTAKE_THRESHOLD = 3.0


class Competitor:
    relative_splits: List[float]
    z_scores: List[float]

    def __init__(self, splits: List[int]) -> None:
        self.splits = splits
        self.total_time = sum(splits)
        self.adjustment_factor = 1.0


class Course:
    def __init__(self, competitors: List[Competitor]) -> None:
        self.competitors = competitors
        self.num_splits = len(competitors[0].splits)

    def set_adjustments(self) -> None:
        """Calculate time adjustment factors.

        This adjustment normalizes each competitor's splits
        based on their overall speed.
        """

        best_time = min(c.total_time for c in self.competitors)
        for c in self.competitors:
            c.adjustment_factor = best_time / c.total_time

    def set_relative_splits(self) -> None:
        for i in range(self.num_splits):
            adjusted_splits = [c.splits[i] * c.adjustment_factor for c in self.competitors]
            # because of the adjustments, some times could be too fast
            # don't consider them when calculating the best split
            best_split = min(remove_outliers(
                adjusted_splits, threshold_low=TOO_FAST_THRESHOLD
            ))
            for c, split in zip(self.competitors, adjusted_splits):
                c.relative_splits[i] = split / best_split

    def calculate_z_scores(self) -> None:
        for i in range(self.num_splits):
            relative_splits = [c.relative_splits[i] for c in self.competitors]
            z_scores = z_score(relative_splits)
            for c, z in zip(self.competitors, z_scores):
                c.z_scores[i] = z


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
