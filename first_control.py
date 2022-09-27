#!/usr/bin/env python3
import datetime
import math
import statistics
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
) -> float:
    print("##########")
    max_controls = max(course.num_controls for course in courses)
    control_mistake_probs: List[List[float]] = [[] for _ in range(max_controls)]
    for course in courses:
        competitors = [
            c for c in course.competitors
            if competitor_predicate(c)
        ]
        if len(competitors) == 0:
            continue
        for control in range(course.num_controls):
            prob = calculate_mistake_prob(competitors, control, threshold)
            control_mistake_probs[control].append(prob)

    # because of competitor filtering, some controls might not have any data
    while len(control_mistake_probs[-1]) == 0:
        control_mistake_probs.pop()

    control_means = [
        statistics.mean(probs)
        for probs in control_mistake_probs
    ]
    # print(" ".join(f"{x:.5f}" for x in control_means))

    first_control_probs = control_mistake_probs[0]
    other_control_probs = [
        prob for probs in control_mistake_probs[1:]
        for prob in probs
    ]
    first_control_mean = statistics.mean(first_control_probs)
    other_control_mean = statistics.mean(other_control_probs)
    print(f"{first_control_mean=:.5f}")
    print(f"{other_control_mean=:.5f}")

    # null hypothesis: mistake probability is always the same
    overall_mean = statistics.mean([
        prob for probs in control_mistake_probs
        for prob in probs
    ])
    var = overall_mean * (1 - overall_mean)
    # test statistic is the difference of means
    difference = first_control_mean - other_control_mean
    difference_var = var * (1 / len(first_control_probs) + 1 / len(other_control_probs))
    p_value = 1 - norm.cdf(difference, scale=math.sqrt(difference_var))
    print(f"{p_value=:.5f}")
    return p_value


def calculate_mistake_prob(
    competitors: List[Competitor],
    control: int,
    threshold: float
) -> float:
    num_splits = 0
    num_mistakes = 0
    for c in competitors:
        if control < len(c.losses):
            num_splits += 1
            if c.made_mistake(control, threshold):
                num_mistakes += 1
    return num_mistakes / num_splits

if __name__ == '__main__':
    main()
