#!/usr/bin/env python3
import statistics
from course import SMALL_MISTAKE_THRESHOLD, Competitor, Course
from datasets import DK_ORIS_ID, DK_NAME, DK_DATE_TO, load_user_races_dataset
from scipy import stats
from typing import Callable, List, Tuple


def main():
    courses = load_user_races_dataset(
        DK_ORIS_ID,
        date_to=DK_DATE_TO
    )
    for course in courses:
        course.set_adjustments()
        course.calculate_losses()

    check_hypothesis(courses, SMALL_MISTAKE_THRESHOLD)
    check_hypothesis(courses, SMALL_MISTAKE_THRESHOLD, lambda x: x.name == DK_NAME)


def check_hypothesis(
    courses: List[Course],
    threshold: float,
    competitor_predicate: Callable[[Competitor], bool] = lambda _: True
) -> float:
    print("##########")
    mistake_probs_after_mistake: List[float] = []
    mistake_probs_after_clean: List[float] = []
    for course in courses:
        competitors = [
            c for c in course.competitors
            if competitor_predicate(c)
        ]
        if len(competitors) == 0:
            continue
        try:
            probs_after_mistake, probs_after_clean = \
                calculate_conditional_mistake_prob(competitors, threshold)
        except ZeroDivisionError:
            # skip this course
            continue
        mistake_probs_after_mistake.append(probs_after_mistake)
        mistake_probs_after_clean.append(probs_after_clean)

    print(f"mistake_prob_after_mistake={statistics.mean(mistake_probs_after_mistake):.5f}")
    print(f"mistake_prob_after_clean  ={statistics.mean(mistake_probs_after_clean):.5f}")

    # null hypothesis: mistake probability is always the same
    # use t-test
    result = stats.ttest_ind(
        mistake_probs_after_mistake, mistake_probs_after_clean,
        alternative="greater"
    )
    pvalue = result.pvalue
    print(f"{pvalue=:.5f}")
    return pvalue


def calculate_conditional_mistake_prob(
    competitors: List[Competitor],
    threshold: float
) -> Tuple[float, float]:
    num_splits_after_mistake = 0
    num_mistakes_after_mistake = 0
    num_splits_after_clean = 0
    num_mistakes_after_clean = 0
    for c in competitors:
        for control in range(1, len(c.losses)):
            mistake_previous = c.made_mistake(control - 1, threshold)
            mistake_this = c.made_mistake(control, threshold)
            if mistake_previous:
                num_splits_after_mistake += 1
                if mistake_this:
                    num_mistakes_after_mistake += 1
            else:
                num_splits_after_clean += 1
                if mistake_this:
                    num_mistakes_after_clean += 1
    return (
        num_mistakes_after_mistake / num_splits_after_mistake,
        num_mistakes_after_clean / num_splits_after_clean
    )


if __name__ == '__main__':
    main()
