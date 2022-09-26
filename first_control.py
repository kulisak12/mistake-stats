#!/usr/bin/env python3
import datetime
from typing import List
from course import SMALL_MISTAKE_THRESHOLD, BIG_MISTAKE_THRESHOLD
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

    competitors = [
        c
        for course in courses
        for c in course.competitors
    ]
    for control in range(max_controls):
        mistakes = 0
        total_splits = 0
        for c in competitors:
            if control < len(c.losses):
                total_splits += 1
                if c.made_mistake(control, SMALL_MISTAKE_THRESHOLD):
                    mistakes += 1
        mistake_percentages.append(mistakes / total_splits)

    print(mistake_percentages)

if __name__ == '__main__':
    main()
