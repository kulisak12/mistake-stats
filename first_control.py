#!/usr/bin/env python3
import datetime
import math
from course import SMALL_MISTAKE_THRESHOLD, BIG_MISTAKE_THRESHOLD, Competitor, Course
from datasets import DK_ORIS_ID, DK_NAME, load_user_races_dataset
from scipy.stats import norm
from typing import Callable, List


def main():
    courses = load_user_races_dataset(
        DK_ORIS_ID,
        date_to=datetime.date(2022, 8, 31)
    )
    for course in courses:
        course.set_adjustments()
        course.calculate_losses()

    check_hypothesis(courses, SMALL_MISTAKE_THRESHOLD)
    check_hypothesis(courses, BIG_MISTAKE_THRESHOLD)
    check_hypothesis(courses, SMALL_MISTAKE_THRESHOLD, lambda x: x.name == DK_NAME)
    check_hypothesis(courses, BIG_MISTAKE_THRESHOLD, lambda x: x.name == DK_NAME)


def check_hypothesis(
    courses: List[Course],
    threshold: float,
    competitor_predicate: Callable[[Competitor], bool] = lambda _: True
) -> None:
    print("##########")
    competitors = [
        c
        for course in courses
        for c in course.competitors
    ]
    competitors = list(filter(competitor_predicate, competitors))

    max_controls = max(len(c.losses) for c in competitors)
    num_mistakes = [0 for _ in range(max_controls)]
    num_splits = [0 for _ in range(max_controls)]
    for control in range(max_controls):
        for c in competitors:
            if control < len(c.losses):
                num_splits[control] += 1
                if c.made_mistake(control, threshold):
                    num_mistakes[control] += 1

    # print mistake percentages
    print([m / s for m, s in zip(num_mistakes, num_splits)])

    first_control_mistakes = num_mistakes[0]
    first_control_splits = num_splits[0]
    first_control_p = first_control_mistakes / first_control_splits
    print(f"{first_control_p=}")
    other_control_mistakes = sum(num_mistakes[1:])
    other_control_splits = sum(num_splits[1:])
    other_control_p = other_control_mistakes / other_control_splits
    print(f"{other_control_p=}")

    # null hypothesis: mistake probability is always the same
    mistake_probability = sum(num_mistakes) / sum(num_splits)
    var = mistake_probability * (1 - mistake_probability)
    # test statistic is the difference of means
    difference = first_control_p - other_control_p
    difference_var = var * (1 / first_control_splits + 1 / other_control_splits)
    p_value = norm.cdf(difference, scale=math.sqrt(difference_var))
    print(f"{p_value=}")


if __name__ == '__main__':
    main()
