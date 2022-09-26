import datetime
from oris import get_user_events, get_splits
from course import Competitor, Course
from typing import Optional, List

DK_ORIS_ID = 40163
MIN_COMPETITORS = 3


def load_user_races_dataset(
    user_id: int,
    date_from: datetime.date = datetime.date.min,
    date_to: datetime.date = datetime.date.today()
) -> List[Course]:
    user_events = get_user_events(user_id, date_from, date_to)
    courses: List[Course] = []
    for event in user_events.values():
        class_id = event["ClassID"]
        splits = get_splits(class_id)
        course = parse_splits(splits)
        if course is not None:
            courses.append(course)
    return courses


def parse_splits(data: dict) -> Optional[Course]:

    def parse_competitor_splits(competitor: dict) -> Optional[List[int]]:
        splits: List[int] = []
        # controls indexing is 1-based
        for i in range(1, num_controls + 1):
            split_str = competitor.get(f"SplitTime{i}")
            # skip competitor if some of their splits are missing
            if not split_str:
                return None
            split = parse_time(split_str)
            splits.append(split)
        return splits

    # no splits for this race
    if len(data) == 0:
        return None

    num_controls = len(data["Controls"]) - 2  # omit finish and last control
    if num_controls <= 0:
        return None
    competitors: List[Competitor] = []
    for competitor in data["Splits"].values():
        parsed = parse_competitor_splits(competitor)
        name = competitor["ResName"]
        if parsed is not None:
            competitors.append(Competitor(parsed, name))

    # it does not make sense to calculate mistakes data
    # for only a few competitors is available
    if len(competitors) < MIN_COMPETITORS:
        return None
    return Course(competitors)


def parse_time(time: str) -> int:
    if ":" not in time:
        x = 0
    minutes, seconds = time.split(":")
    return 60 * int(minutes) + int(seconds)


load_user_races_dataset(DK_ORIS_ID)
