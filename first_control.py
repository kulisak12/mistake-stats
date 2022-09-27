#!/usr/bin/env python3
import statistics
from course import SMALL_MISTAKE_THRESHOLD, BIG_MISTAKE_THRESHOLD, Competitor, Course
from datasets import DK_ORIS_ID, DK_NAME, DK_DATE_TO, load_user_races_dataset
from scipy import stats
from typing import Callable, List


def main():
    courses = load_user_races_dataset(
        DK_ORIS_ID,
        date_to=DK_DATE_TO
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

    first_control_probs = control_mistake_probs[0]
    other_control_probs = [
        prob for probs in control_mistake_probs[1:]
        for prob in probs
    ]
    print(f"first_control_mean={statistics.mean(first_control_probs):.5f}")
    print(f"other_control_mean={statistics.mean(other_control_probs):.5f}")

    # null hypothesis: mistake probability is always the same
    # use t-test
    result = stats.ttest_ind(
        first_control_probs, other_control_probs,
        alternative="greater"
    )
    pvalue = result.pvalue
    print(f"{pvalue=:.5f}")
    return pvalue


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
