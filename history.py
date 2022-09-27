#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
from course import SMALL_MISTAKE_THRESHOLD, Course
from datasets import DK_ORIS_ID, DK_NAME, DK_DATE_TO, load_user_races_dataset
from scipy import stats
from typing import List


def main():
    courses = load_user_races_dataset(
        DK_ORIS_ID,
        date_to=DK_DATE_TO
    )
    for course in courses:
        course.set_adjustments()
        course.calculate_losses()

    analyze_history(courses, SMALL_MISTAKE_THRESHOLD, DK_NAME)


def analyze_history(
    courses: List[Course],
    threshold: float,
    name: str,
) -> float:
    my_races = [
        c for course in courses
        for c in course.competitors
        if c.name == name
    ]
    mistake_counts: List[int] = []
    mistake_probs: List[float] = []
    for me in my_races:
        num_mistakes = 0
        for control in range(len(me.losses)):
            if me.made_mistake(control, threshold):
                num_mistakes += 1
        mistake_counts.append(num_mistakes)
        mistake_probs.append(num_mistakes / len(me.losses))

    time_axis = np.arange(1, len(my_races) + 1)
    counts_linreg_result = stats.linregress(time_axis, mistake_counts)
    probs_linreg_result = stats.linregress(time_axis, mistake_probs)
    print(f"Counts slope: {counts_linreg_result.slope} +- {counts_linreg_result.stderr}")
    print(f"Probs slope:  {probs_linreg_result.slope} +- {probs_linreg_result.stderr}")

    plt.plot(time_axis, mistake_probs, "o")
    plt.plot(time_axis, time_axis * probs_linreg_result.slope + probs_linreg_result.intercept, linestyle="dashed")
    plt.xlabel("Závod")
    plt.ylabel("Procento chyb")
    # plt.show()
    plt.savefig("history-probs.png")
    plt.clf()


if __name__ == '__main__':
    main()
