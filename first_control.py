#!/usr/bin/env python3
import datetime
from typing import List
from course import Course, SMALL_MISTAKE_THRESHOLD, BIG_MISTAKE_THRESHOLD
from datasets import DK_ORIS_ID, load_user_races_dataset


def main():
    courses = load_user_races_dataset(
        DK_ORIS_ID,
        date_to=datetime.date(2022, 8, 31)
    )
    for course in courses:
        course.set_adjustments()
        course.set_relative_splits()
        course.calculate_z_scores()

    max_controls = max(course.num_controls for course in courses)
    mistake_splits: List[int] = []
    total_splits: List[int] = []
    for control in range(max_controls):
        mistakes = sum(
            count_mistakes_for_control(course, control, SMALL_MISTAKE_THRESHOLD)
            for course in courses
        )
        total = sum(
            len(course.competitors)
            for course in courses
            if control < course.num_controls
        )
        mistake_splits.append(mistakes)
        total_splits.append(total)

    mistake_percentage = [mistake / total for mistake, total in zip(mistake_splits, total_splits)]
    print(mistake_percentage)


def count_mistakes_for_control(course: Course, control: int, threshold: float) -> int:
    num_mistakes = 0
    for c in course.competitors:
        if len(c.z_scores) > control and c.z_scores[control] > threshold:
            num_mistakes += 1
    return num_mistakes


if __name__ == '__main__':
    main()
