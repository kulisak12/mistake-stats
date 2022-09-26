#!/usr/bin/env python3
import datetime
from typing import List, Tuple
from course import Course, SMALL_MISTAKE_THRESHOLD, BIG_MISTAKE_THRESHOLD
from datasets import DK_ORIS_ID, load_user_races_dataset


def main():
    courses = load_user_races_dataset(
        DK_ORIS_ID,
        date_to=datetime.date(2022, 8, 31)
    )
    for course in courses:
        course.set_adjustments()
        course.calculate_losses()

    max_controls = max(course.num_controls for course in courses)
    mistake_percentages: List[float] = []
    for control in range(max_controls):
        mistakes_sum = 0
        total_sum = 0
        for course in courses:
            mistakes, total = count_mistakes_for_control(
                course, control, SMALL_MISTAKE_THRESHOLD
            )
            mistakes_sum += mistakes
            total_sum += total
        mistake_percentages.append(mistakes_sum / total_sum)

    print(mistake_percentages)


def count_mistakes_for_control(course: Course, control: int, threshold: float) -> Tuple[int, int]:
    """Return number of mistakes and total number of considered splits."""

    num_mistakes = 0
    num_splits = 0
    for c in course.competitors:
        if control < len(c.losses):
            num_splits += 1
            if c.made_mistake(control, threshold):
                num_mistakes += 1
    return num_mistakes, num_splits


if __name__ == '__main__':
    main()
